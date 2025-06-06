
import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { Plus, Search, Edit, Trash2 } from "lucide-react";

interface Product {
  id: number;
  name: string;
  category: string;
  stockLevel: number;
  reorderThreshold: number;
}

const mockProducts: Product[] = [
  { id: 1, name: "Gaming Laptop", category: "Electronics", stockLevel: 45, reorderThreshold: 20 },
  { id: 2, name: "Wireless Monitor", category: "Electronics", stockLevel: 12, reorderThreshold: 25 },
  { id: 3, name: "Mechanical Keyboard", category: "Accessories", stockLevel: 67, reorderThreshold: 30 },
  { id: 4, name: "Gaming Mouse", category: "Accessories", stockLevel: 23, reorderThreshold: 15 },
  { id: 5, name: "USB Cable", category: "Accessories", stockLevel: 89, reorderThreshold: 50 },
];

export function ProductManager() {
  const [products, setProducts] = useState<Product[]>(mockProducts);
  const [searchTerm, setSearchTerm] = useState("");
  const [isAddingProduct, setIsAddingProduct] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);

  const filteredProducts = products.filter(product =>
    product.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    product.category.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getStockStatus = (current: number, threshold: number) => {
    if (current <= threshold) return { status: "Low Stock", variant: "destructive" as const };
    if (current <= threshold * 1.5) return { status: "Warning", variant: "secondary" as const };
    return { status: "In Stock", variant: "default" as const };
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Product Management</h1>
          <p className="text-muted-foreground">
            Manage your inventory and stock levels
          </p>
        </div>
        <Button onClick={() => setIsAddingProduct(true)}>
          <Plus className="mr-2 h-4 w-4" />
          Add Product
        </Button>
      </div>

      {/* Search Bar */}
      <Card>
        <CardContent className="pt-6">
          <div className="relative">
            <Search className="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search products..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-8"
            />
          </div>
        </CardContent>
      </Card>

      {/* Products Grid */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {filteredProducts.map((product) => {
          const stockStatus = getStockStatus(product.stockLevel, product.reorderThreshold);
          
          return (
            <Card key={product.id}>
              <CardHeader>
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="text-lg">{product.name}</CardTitle>
                    <CardDescription>{product.category}</CardDescription>
                  </div>
                  <div className="flex space-x-1">
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => setEditingProduct(product)}
                    >
                      <Edit className="h-4 w-4" />
                    </Button>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => {
                        setProducts(products.filter(p => p.id !== product.id));
                      }}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Stock Level:</span>
                    <span className="text-lg font-bold">{product.stockLevel}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Reorder Threshold:</span>
                    <span className="text-sm">{product.reorderThreshold}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-medium">Status:</span>
                    <Badge variant={stockStatus.variant}>
                      {stockStatus.status}
                    </Badge>
                  </div>
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>

      {filteredProducts.length === 0 && (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-6">
              <p className="text-muted-foreground">No products found matching your search.</p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Add/Edit Product Modal would go here */}
      {isAddingProduct && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <Card className="w-full max-w-md">
            <CardHeader>
              <CardTitle>Add New Product</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <Label htmlFor="name">Product Name</Label>
                  <Input id="name" placeholder="Enter product name" />
                </div>
                <div>
                  <Label htmlFor="category">Category</Label>
                  <Input id="category" placeholder="Enter category" />
                </div>
                <div>
                  <Label htmlFor="stock">Stock Level</Label>
                  <Input id="stock" type="number" placeholder="Enter stock level" />
                </div>
                <div>
                  <Label htmlFor="threshold">Reorder Threshold</Label>
                  <Input id="threshold" type="number" placeholder="Enter reorder threshold" />
                </div>
                <div className="flex space-x-2">
                  <Button onClick={() => setIsAddingProduct(false)} variant="outline">
                    Cancel
                  </Button>
                  <Button onClick={() => setIsAddingProduct(false)}>
                    Add Product
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
