
import { useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { AlertTriangle, CheckCircle, Clock, Bell } from "lucide-react";

interface StockAlert {
  id: number;
  productId: number;
  productName: string;
  alertType: 'low_stock' | 'reorder_needed' | 'excess_stock' | 'forecast_anomaly';
  message: string;
  status: 'new' | 'acknowledged' | 'resolved';
  createdAt: string;
  priority: 'low' | 'medium' | 'high' | 'critical';
}

const mockAlerts: StockAlert[] = [
  {
    id: 1,
    productId: 2,
    productName: "Wireless Monitor",
    alertType: "low_stock",
    message: "Stock level (12 units) is below reorder threshold (25 units)",
    status: "new",
    createdAt: "2024-01-15T10:30:00Z",
    priority: "high"
  },
  {
    id: 2,
    productId: 4,
    productName: "Gaming Mouse",
    alertType: "reorder_needed",
    message: "Predicted to reach reorder threshold in 5 days based on current demand",
    status: "new",
    createdAt: "2024-01-15T09:15:00Z",
    priority: "medium"
  },
  {
    id: 3,
    productId: 1,
    productName: "Gaming Laptop",
    alertType: "forecast_anomaly",
    message: "Unusual spike in demand detected. Consider increasing stock levels",
    status: "acknowledged",
    createdAt: "2024-01-14T16:45:00Z",
    priority: "medium"
  },
  {
    id: 4,
    productId: 3,
    productName: "Mechanical Keyboard",
    alertType: "excess_stock",
    message: "Stock level significantly above normal. Consider reducing orders",
    status: "resolved",
    createdAt: "2024-01-14T11:20:00Z",
    priority: "low"
  }
];

export function AlertCenter() {
  const [alerts, setAlerts] = useState<StockAlert[]>(mockAlerts);
  const [filter, setFilter] = useState<'all' | 'new' | 'acknowledged' | 'resolved'>('all');

  const filteredAlerts = filter === 'all' ? alerts : alerts.filter(alert => alert.status === filter);
  const newAlerts = alerts.filter(alert => alert.status === 'new').length;
  const criticalAlerts = alerts.filter(alert => alert.priority === 'critical').length;

  const updateAlertStatus = (id: number, newStatus: StockAlert['status']) => {
    setAlerts(alerts.map(alert => 
      alert.id === id ? { ...alert, status: newStatus } : alert
    ));
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'text-red-600 bg-red-50 border-red-200';
      case 'high': return 'text-orange-600 bg-orange-50 border-orange-200';
      case 'medium': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
      case 'low': return 'text-blue-600 bg-blue-50 border-blue-200';
      default: return 'text-gray-600 bg-gray-50 border-gray-200';
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'new':
        return <Badge variant="destructive">New</Badge>;
      case 'acknowledged':
        return <Badge variant="secondary">Acknowledged</Badge>;
      case 'resolved':
        return <Badge variant="default">Resolved</Badge>;
      default:
        return <Badge>Unknown</Badge>;
    }
  };

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'low_stock':
      case 'reorder_needed':
        return <AlertTriangle className="h-4 w-4" />;
      case 'forecast_anomaly':
        return <Bell className="h-4 w-4" />;
      default:
        return <Clock className="h-4 w-4" />;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Alert Center</h1>
          <p className="text-muted-foreground">
            Monitor and manage inventory alerts
          </p>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" onClick={() => setFilter('all')}>
            All
          </Button>
          <Button variant="outline" onClick={() => setFilter('new')}>
            New ({newAlerts})
          </Button>
          <Button variant="outline" onClick={() => setFilter('acknowledged')}>
            Acknowledged
          </Button>
          <Button variant="outline" onClick={() => setFilter('resolved')}>
            Resolved
          </Button>
        </div>
      </div>

      {/* Alert Summary */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">New Alerts</CardTitle>
            <AlertTriangle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">{newAlerts}</div>
            <p className="text-xs text-muted-foreground">Require attention</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Critical Alerts</CardTitle>
            <Bell className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">{criticalAlerts}</div>
            <p className="text-xs text-muted-foreground">Immediate action needed</p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Alerts</CardTitle>
            <CheckCircle className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{alerts.length}</div>
            <p className="text-xs text-muted-foreground">All time</p>
          </CardContent>
        </Card>
      </div>

      {/* Critical Alerts Banner */}
      {criticalAlerts > 0 && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>
            <strong>Critical Alert:</strong> {criticalAlerts} critical {criticalAlerts === 1 ? 'alert requires' : 'alerts require'} immediate attention
          </AlertDescription>
        </Alert>
      )}

      {/* Alerts List */}
      <div className="space-y-4">
        {filteredAlerts.map((alert) => (
          <Card key={alert.id} className={`border-l-4 ${getPriorityColor(alert.priority)}`}>
            <CardHeader>
              <div className="flex justify-between items-start">
                <div className="flex items-center space-x-2">
                  {getAlertIcon(alert.alertType)}
                  <div>
                    <CardTitle className="text-lg">{alert.productName}</CardTitle>
                    <CardDescription className="capitalize">
                      {alert.alertType.replace('_', ' ')} • {alert.priority} priority
                    </CardDescription>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  {getStatusBadge(alert.status)}
                  <Badge variant="outline" className="capitalize">
                    {alert.priority}
                  </Badge>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <p className="text-sm mb-4">{alert.message}</p>
              <div className="flex justify-between items-center">
                <p className="text-xs text-muted-foreground">
                  Created: {new Date(alert.createdAt).toLocaleString()}
                </p>
                <div className="flex space-x-2">
                  {alert.status === 'new' && (
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => updateAlertStatus(alert.id, 'acknowledged')}
                    >
                      Acknowledge
                    </Button>
                  )}
                  {alert.status === 'acknowledged' && (
                    <Button
                      size="sm"
                      onClick={() => updateAlertStatus(alert.id, 'resolved')}
                    >
                      Mark Resolved
                    </Button>
                  )}
                  {alert.status === 'resolved' && (
                    <Button
                      size="sm"
                      variant="outline"
                      onClick={() => updateAlertStatus(alert.id, 'new')}
                    >
                      Reopen
                    </Button>
                  )}
                </div>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {filteredAlerts.length === 0 && (
        <Card>
          <CardContent className="pt-6">
            <div className="text-center py-6">
              <CheckCircle className="mx-auto h-12 w-12 text-green-500 mb-4" />
              <p className="text-lg font-medium">No alerts found</p>
              <p className="text-muted-foreground">
                {filter === 'all' 
                  ? "All clear! No alerts at this time." 
                  : `No ${filter} alerts found.`
                }
              </p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
