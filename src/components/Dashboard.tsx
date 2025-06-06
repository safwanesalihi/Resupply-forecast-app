
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Progress } from "@/components/ui/progress";
import { Badge } from "@/components/ui/badge";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from "recharts";
import { Package, TrendingUp, AlertTriangle, DollarSign } from "lucide-react";

// Mock data for dashboard
const mockStockData = [
  { name: 'Laptops', current: 45, threshold: 20, forecast: 15 },
  { name: 'Monitors', current: 12, threshold: 25, forecast: 8 },
  { name: 'Keyboards', current: 67, threshold: 30, forecast: 45 },
  { name: 'Mice', current: 23, threshold: 15, forecast: 12 },
];

const mockSalesData = [
  { month: 'Jan', sales: 4000, forecast: 3800 },
  { month: 'Feb', sales: 3000, forecast: 3200 },
  { month: 'Mar', sales: 5000, forecast: 4800 },
  { month: 'Apr', sales: 4500, forecast: 4600 },
  { month: 'May', sales: 6000, forecast: 5800 },
  { month: 'Jun', sales: 5500, forecast: 5600 },
];

export function Dashboard() {
  const totalProducts = 156;
  const lowStockItems = 8;
  const forecastAccuracy = 94.2;
  const totalValue = 125000;

  const criticalItems = mockStockData.filter(item => item.current <= item.threshold);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
        <p className="text-muted-foreground">
          Welcome to your Intelligent Stock Management System
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Products</CardTitle>
            <Package className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{totalProducts}</div>
            <p className="text-xs text-muted-foreground">+12% from last month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Low Stock Items</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">{lowStockItems}</div>
            <p className="text-xs text-muted-foreground">Requires attention</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Forecast Accuracy</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{forecastAccuracy}%</div>
            <p className="text-xs text-muted-foreground">+2.1% from last month</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Inventory Value</CardTitle>
            <DollarSign className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">${totalValue.toLocaleString()}</div>
            <p className="text-xs text-muted-foreground">+5.2% from last month</p>
          </CardContent>
        </Card>
      </div>

      {/* Critical Alerts */}
      {criticalItems.length > 0 && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            <strong>Critical Stock Alert:</strong> {criticalItems.length} items are below reorder threshold
          </AlertDescription>
        </Alert>
      )}

      <div className="grid gap-6 md:grid-cols-2">
        {/* Stock Levels Chart */}
        <Card>
          <CardHeader>
            <CardTitle>Current Stock Levels</CardTitle>
            <CardDescription>
              Stock levels vs reorder thresholds
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={mockStockData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="current" fill="#3b82f6" name="Current Stock" />
                <Bar dataKey="threshold" fill="#ef4444" name="Threshold" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Sales vs Forecast */}
        <Card>
          <CardHeader>
            <CardTitle>Sales vs Forecast</CardTitle>
            <CardDescription>
              Actual sales performance compared to AI predictions
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={mockSalesData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="sales" stroke="#3b82f6" name="Actual Sales" />
                <Line type="monotone" dataKey="forecast" stroke="#10b981" strokeDasharray="5 5" name="Forecast" />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Product Status Overview */}
      <Card>
        <CardHeader>
          <CardTitle>Product Status Overview</CardTitle>
          <CardDescription>
            Detailed view of current inventory status
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {mockStockData.map((item) => (
              <div key={item.name} className="flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="min-w-0 flex-1">
                    <p className="text-sm font-medium">{item.name}</p>
                    <p className="text-sm text-muted-foreground">
                      {item.current} units in stock
                    </p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <Badge 
                    variant={item.current <= item.threshold ? "destructive" : "default"}
                  >
                    {item.current <= item.threshold ? "Low Stock" : "In Stock"}
                  </Badge>
                  <div className="w-24">
                    <Progress 
                      value={(item.current / (item.threshold * 2)) * 100} 
                      className="h-2"
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
