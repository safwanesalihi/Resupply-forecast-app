from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

from app.api.v1.deps import get_db, get_current_user
from app.schemas.sales import RawSales, CleanSales, SalesImport
from app.db.models.sales import RawSales as RawSalesModel, CleanSales as CleanSalesModel
from app.db.models.user import User
from app.db.models.product import Product # Import Product model
from app.services.dynamics_bc import DynamicsBCService

router = APIRouter()

def process_and_save_sales(db: Session, sales_data: List[dict]):
    """Helper function to process and save sales data in the background."""
    raw_count = 0
    clean_count = 0
    processed_ids = set()

    # Get existing product IDs from the database for validation
    existing_product_ids = {p.id for p in db.query(Product.id).all()}

    for sale in sales_data:
        # Map Dynamics BC fields to our model
        # Adjust field mappings based on actual Dynamics BC API response
        # Assuming 'itemId' from BC corresponds to our 'product_id'
        # Assuming 'postingDate' is the sale date
        # Assuming 'quantity' represents sales quantity (needs to be positive)
        # Assuming 'entryType' indicates if it's a sale
        
        try:
            # Use .get() with defaults to handle potentially missing keys
            bc_item_id_str = sale.get("itemId") # BC Item ID might be a GUID string
            # Find corresponding internal product ID. Requires a mapping or matching logic.
            # For this example, we'll try to find a product with a matching name or number if ID fails.
            # This mapping logic needs refinement based on how BC items relate to your Product model.
            product_id = None
            if bc_item_id_str:
                 # Simplistic: Assume internal ID matches BC ID for now. Needs proper mapping.
                 # product = db.query(Product).filter(Product.dynamics_bc_id == bc_item_id_str).first()
                 # if product: product_id = product.id
                 # TEMPORARY: If ID is numeric string, try converting
                 try:
                     potential_id = int(bc_item_id_str)
                     if potential_id in existing_product_ids:
                         product_id = potential_id
                 except ValueError:
                     pass # BC ID might not be an integer

            if not product_id:
                # print(f"Skipping sale: Could not map BC item ID ")
                continue # Skip if product mapping fails

            sale_date_str = sale.get("postingDate", ")
            if not sale_date_str:
                continue
            sale_date = date.fromisoformat(sale_date_str.split("T")[0])
            
            quantity = abs(int(sale.get("quantity", 0)))
            entry_type = sale.get("entryType")

            # Skip non-sales entries or zero quantity
            if quantity <= 0 or entry_type != "Sale":
                continue

            # Avoid duplicates within this batch (simple check)
            sale_key = (product_id, sale_date, quantity)
            if sale_key in processed_ids:
                continue
            processed_ids.add(sale_key)

            # Save as raw sales
            raw_sale = RawSalesModel(
                product_id=product_id,
                date=sale_date,
                quantity=quantity
            )
            db.add(raw_sale)
            raw_count += 1
            
            # Also save as clean sales (in a real app, apply cleaning logic here)
            clean_sale = CleanSalesModel(
                product_id=product_id,
                date=sale_date,
                quantity=quantity
            )
            db.add(clean_sale)
            clean_count += 1

        except Exception as e:
            print(f"Error processing sale record {sale.get("id", "N/A")}: {e}")
            # Optionally log the error and continue with the next record
            continue

    try:
        db.commit()
        print(f"Successfully committed {raw_count} raw and {clean_count} clean sales records.")
    except Exception as e:
        db.rollback()
        print(f"Database commit failed: {e}")

@router.get("/raw", response_model=List[RawSales])
def get_raw_sales(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    product_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
) -> List[RawSales]:
    """
    Get raw sales data with optional filtering
    """
    query = db.query(RawSalesModel)
    
    if product_id:
        query = query.filter(RawSalesModel.product_id == product_id)
    if start_date:
        query = query.filter(RawSalesModel.date >= start_date)
    if end_date:
        query = query.filter(RawSalesModel.date <= end_date)
    
    return query.order_by(RawSalesModel.date.desc()).offset(skip).limit(limit).all()

@router.get("/clean", response_model=List[CleanSales])
def get_clean_sales(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    product_id: Optional[int] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    current_user: User = Depends(get_current_user),
) -> List[CleanSales]:
    """
    Get cleaned sales data with optional filtering
    """
    query = db.query(CleanSalesModel)
    
    if product_id:
        query = query.filter(CleanSalesModel.product_id == product_id)
    if start_date:
        query = query.filter(CleanSalesModel.date >= start_date)
    if end_date:
        query = query.filter(CleanSalesModel.date <= end_date)
    
    return query.order_by(CleanSalesModel.date.desc()).offset(skip).limit(limit).all()

@router.post("/import", status_code=status.HTTP_202_ACCEPTED)
def import_sales_data(
    import_data: SalesImport,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict:
    """
    Trigger background task to import sales data from Dynamics BC.
    Requires proper mapping between internal Product IDs and Dynamics BC Item IDs.
    """
    try:
        bc_service = DynamicsBCService()
        
        # Format dates for Dynamics BC API
        start_date_str = import_data.start_date.isoformat()
        end_date_str = import_data.end_date.isoformat()
        
        # Get sales data from Dynamics BC
        # Note: Mapping internal product IDs to BC item IDs is crucial here.
        # This example assumes a direct mapping or fetches all if no IDs provided.
        # You might need a lookup service or store BC IDs in your Product model.
        sales_data_from_bc = []
        if import_data.product_ids:
             # Fetch existing products to get their BC IDs (assuming stored)
             # products_to_fetch = db.query(Product).filter(Product.id.in_(import_data.product_ids)).all()
             # bc_item_ids = [p.dynamics_bc_id for p in products_to_fetch if p.dynamics_bc_id]
             # This part needs refinement based on your mapping strategy
             print("Warning: Importing sales for specific product IDs requires mapping to Dynamics BC Item IDs.")
             # Fetching all for now as mapping is not implemented
             sales_data_from_bc = bc_service.get_item_ledger_entries(
                 start_date=start_date_str,
                 end_date=end_date_str
             )
        else:
            sales_data_from_bc = bc_service.get_item_ledger_entries(
                start_date=start_date_str,
                end_date=end_date_str
            )

        if not sales_data_from_bc:
             return {"status": "success", "message": "No sales data found in Dynamics BC for the specified criteria."} 

        # Add the processing task to the background
        background_tasks.add_task(process_and_save_sales, db, sales_data_from_bc)
        
        return {
            "status": "accepted",
            "message": f"Sales data import started in the background. Found {len(sales_data_from_bc)} potential records."
        }
    
    except Exception as e:
        # Log the exception details
        print(f"Error initiating sales data import: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start sales data import: {str(e)}"
        )

