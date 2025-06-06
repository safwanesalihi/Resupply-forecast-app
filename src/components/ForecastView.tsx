
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from "recharts";
import { TrendingUp, Calendar, Target } from "lucide-react";

const mockForecastData = [
  { date: '2024-01', actual: 120, predicted: 118, accuracy: 98.3 },
  { date: '2024-02', actual: 98, predicted: 102, accuracy: 96.1 },
  { date: '2024-03', actual: 145, predicted: 140, accuracy: 96.6 },
  { date: '2024-04', actual: 132, predicted: 135, accuracy: 97.7 },
  { date: '2024-05', actual: 167, predicted: 165, accuracy: 98.8 },
  { date: '2024-06', actual: null, predicted: 155, accuracy: null },
  { date: '2024-07', actual: null, predicted: 172, accuracy: null },
  { date: '2024-08', actual: null, predicted: 180, accuracy: null },
];

const productForecasts = [
  { name: "Gaming Laptop", currentStock: 45, predicted7days: 38, predicted30days: 25, trend: "decreasing" },
  { name: "Wireless Monitor", currentStock: 12, predicted7days: 8, predicted30days: 2, trend: "critical" },
  { name: "Mechanical Keyboard", currentStock: 67, predicted7days: 58, predicted30days: 35, trend: "stable" },
  { name: "Gaming Mouse", currentStock: 23, predicted7days: 18, predicted30days: 8, trend: "decreasing" },
];

export function ForecastView() {
  const overallAccuracy = 97.5;
  const nextMonthDemand = 155;
  const reorderSuggestions = 3;

  const getTrendBadge = (trend: string) => {
    switch (trend) {
      case "critical":
        return <Badge variant="destructive">Critical</Badge>;
      case "decreasing":
        return <Badge variant="secondary">Decreasing</Badge>;
      case "stable":
        return <Badge variant="default">Stable</Badge>;
      default:
        return <Badge>Unknown</Badge>;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">AI Forecasting</h1>
          <p className="text-muted-foreground">
            Predictive analytics for inventory management
          </p>
        </div>
        <Button>
          <TrendingUp className="mr-2 h-4 w-4" />
          Generate New Forecast
        </Button>
      </div>

      {/* Key Forecast Metrics */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Forecast Accuracy</CardTitle>
            <Target className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{overallAccuracy}%</div>
            <p className="text-xs text-muted-foreground">Last 6 months average</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Next Month Demand</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{nextMonthDemand}</div>
            <p className="text-xs text-muted-foreground">Units predicted</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Reorder Suggestions</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">{reorderSuggestions}</div>
            <p className="text-xs text-muted-foreground">Products need attention</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        {/* Historical vs Predicted */}
        <Card>
          <CardHeader>
            <CardTitle>Historical vs Predicted Demand</CardTitle>
            <CardDescription>
              Actual sales data compared to AI predictions
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={mockForecastData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Line 
                  type="monotone" 
                  dataKey="actual" 
                  stroke="#3b82f6" 
                  name="Actual Sales"
                  strokeWidth={2}
                />
                <Line 
                  type="monotone" 
                  dataKey="predicted" 
                  stroke="#10b981" 
                  strokeDasharray="5 5" 
                  name="Predicted"
                  strokeWidth={2}
                />
              </LineChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        {/* Forecast Accuracy */}
        <Card>
          <CardHeader>
            <CardTitle>Forecast Accuracy Trend</CardTitle>
            <CardDescription>
              Monthly accuracy of AI predictions
            </CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={mockForecastData.filter(d => d.accuracy)}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis domain={[90, 100]} />
                <Tooltip />
                <Bar dataKey="accuracy" fill="#8b5cf6" name="Accuracy %" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Product-Specific Forecasts */}
      <Card>
        <CardHeader>
          <CardTitle>Product Demand Forecasts</CardTitle>
          <CardDescription>
            AI-driven predictions for individual products
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {productForecasts.map((product, index) => (
              <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex-1">
                  <h3 className="font-medium">{product.name}</h3>
                  <p className="text-sm text-muted-foreground">
                    Current Stock: {product.currentStock} units
                  </p>
                </div>
                <div className="flex items-center space-x-6 text-sm">
                  <div className="text-center">
                    <p className="font-medium">{product.predicted7days}</p>
                    <p className="text-muted-foreground">7 days</p>
                  </div>
                  <div className="text-center">
                    <p className="font-medium">{product.predicted30days}</p>
                    <p className="text-muted-foreground">30 days</p>
                  </div>
                  <div>
                    {getTrendBadge(product.trend)}
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
