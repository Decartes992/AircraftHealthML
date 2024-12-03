import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Form, Spinner, Alert, Button } from 'react-bootstrap';
import { ResponsiveLine } from '@nivo/line';
import { LineChart } from 'lucide-react'; // Add icon library
import './NGAFIDDashboard.css'; // Add CSS file

const NGAFIDDashboard = () => {
    const [experiments, setExperiments] = useState([]);
    const [selectedExperiment, setSelectedExperiment] = useState(null);
    const [maintenanceData, setMaintenanceData] = useState(null);
    const [experimentInfo, setExperimentInfo] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [activeCategory, setActiveCategory] = useState('before');

    // Load flight data
    useEffect(() => {
        const loadData = async () => {
            try {
                const response = await fetch('/api/ngafid/flight_data/');
                const data = await response.json();
                setExperiments(data.experiments);
            } catch (error) {
                console.error("Error loading NGAFID data:", error);
                setError('Failed to load NGAFID data');
            }
        };
        loadData();
    }, []);

    // Load selected experiment data
    useEffect(() => {
        const loadExperiment = async (id) => {
            try {
                setLoading(true);
                setError(null);
                const response = await fetch(`/api/ngafid/flight_data/${id}/`);
                const data = await response.json();

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                setExperimentInfo(data.experiment_info);
                setMaintenanceData(processMaintenanceData(data.maintenance_data));
                setLoading(false);
            } catch (error) {
                console.error('Error loading experiment data:', error);
                setError(`Error loading experiment data: ${error.message}`);
                setLoading(false);
            }
        };

        if (selectedExperiment) {
            loadExperiment(selectedExperiment);
        }
    }, [selectedExperiment]);

    // Process maintenance data
    const processMaintenanceData = (data) => {
        const processedData = data.map(item => ({
            before_after: item.before_after,
            date_diff: item.date_diff,
            flight_length: item.flight_length,
            label: item.label,
            number_flights_before: item.number_flights_before,
        }));
        return processedData;
    };

    // Handle category change
    const handleCategoryChange = (category) => {
        setActiveCategory(category);
    };

    // Render maintenance chart
    const renderMaintenanceChart = () => {
        const filteredData = maintenanceData.filter(item => item.before_after === activeCategory);
        const chartData = filteredData.map(item => ({
            x: item.date_diff,
            y: item.flight_length,
            label: item.label,
            number_flights_before: item.number_flights_before,
        }));

        return (
            <ResponsiveLine
                data={[{
                    id: activeCategory,
                    data: chartData
                }]}
                margin={{ top: 20, right: 20, bottom: 50, left: 60 }}
                xScale={{ type: 'point' }}
                yScale={{ type: 'linear', min: 'auto', max: 'auto' }}
                axisBottom={{ 
                    legend: 'Date Difference', 
                    legendOffset: 36, 
                    legendPosition: 'middle',
                    tickRotation: -45,
                    tickPadding: 5,
                    tickSize: 5,
                    format: '%Y-%m-%d' // Adjust based on date format
                }}
                axisLeft={{ 
                    legend: 'Flight Length (hrs)', 
                    legendOffset: -50, 
                    legendPosition: 'middle',
                    tickPadding: 5,
                    tickSize: 5
                }}
                enablePoints={false}
                enableGridX={true}
                enableGridY={true}
                enableCrosshair={true}
                useMesh={true}
                animate={true}
                motionConfig="gentle"
                colors={{ scheme: 'category10' }}
                theme={{
                    axis: {
                        domain: {
                            line: {
                                stroke: '#ffffff',
                                strokeWidth: 1
                            }
                        },
                        legend: {
                            text: {
                                fill: '#ffffff',
                                fontSize: 12
                            }
                        },
                        ticks: {
                            line: {
                                stroke: '#ffffff',
                                strokeWidth: 1
                            },
                            text: {
                                fill: '#ffffff',
                                fontSize: 11
                            }
                        }
                    },
                    grid: {
                        line: {
                            stroke: '#444444',
                            strokeWidth: 1
                        }
                    },
                    legends: {
                        text: {
                            fill: '#ffffff',
                            fontSize: 11
                        }
                    },
                    tooltip: {
                        container: {
                            background: '#333333',
                            color: '#ffffff',
                            fontSize: 12
                        }
                    }
                }}
                tooltip={({ point }) => (
                    <div
                        style={{
                            background: "white",
                            padding: "5px 10px",
                            borderRadius: "3px",
                            boxShadow: "0 2px 6px rgba(0,0,0,0.15)",
                            color: "#000",
                        }}
                    >
                        <strong>{point.serieId}</strong>
                        <br />
                        Date Diff: {point.data.xFormatted}
                        <br />
                        Flight Length: {point.data.yFormatted} hrs
                    </div>
                )}
                onClick={(point) => {
                    alert(`Category: ${activeCategory.toUpperCase()}\nDate Diff: ${point.data.xFormatted}\nFlight Length: ${point.data.yFormatted} hrs`);
                }}
                legends={[
                    {
                        anchor: "bottom-right",
                        direction: "column",
                        translateX: 100,
                        itemWidth: 80,
                        itemHeight: 20,
                        symbolSize: 12,
                        symbolShape: "circle",
                        onClick: (legendItem) => {
                            // Implement legend click if needed
                        },
                        effects: [
                            {
                                on: "hover",
                                style: {
                                    itemBackground: "rgba(0, 0, 0, .03)",
                                    itemOpacity: 1
                                }
                            }
                        ]
                    },
                ]}
                ariaLabel={`${activeCategory.toUpperCase()} Maintenance Line Chart`}
                ariaLive="polite"
            />
        );
    };

    return (
        <div className="min-h-screen bg-dark text-white">
            {/* Header Section */}
            <div
                className="py-4 text-center"
                style={{
                    background: "linear-gradient(to right, #1e3a8a, #2563eb)",
                    color: "white",
                }}
            >
                <h1 className="display-6 font-weight-bold mb-1">
                    <LineChart size={40} className="mb-2" /> NGAFID Maintenance Dataset Dashboard
                </h1>
                <p className="mb-0">Analyze and visualize NGAFID maintenance trends and flight data.</p>
            </div>

            <Container className="my-4">
                {/* Main Control Section */}
                <Card className="shadow-lg section-padding card-padding">
                    <Card.Body>
                        <Row className="card-container">
                            <Col md={6} className="card-column">
                                {/* Select Flight or Maintenance Event */}
                                <Card className="shadow-sm mb-3 card-item nested-card">
                                    <Card.Body className="py-2 px-3">
                                        <Form.Group>
                                            <Form.Label className="mb-1">Select Flight or Maintenance Event</Form.Label>
                                            <Form.Select 
                                                value={selectedExperiment || ''}
                                                onChange={(e) => setSelectedExperiment(e.target.value)}
                                                className="bg-dark text-white py-1"
                                            >
                                                <option value="">Choose an event...</option>
                                                {experiments.map(exp => (
                                                    <option key={exp.master_index} value={exp.master_index}>{exp.label}</option>
                                                ))}
                                            </Form.Select>
                                        </Form.Group>
                                    </Card.Body>
                                </Card>

                                {/* Maintenance Categories Buttons */}
                                <Card className="shadow-sm card-item nested-card">
                                    <Card.Body className="py-2 px-3">
                                        <h5 className="mb-2" style={{ fontWeight: "bold" }}>Maintenance Categories</h5>
                                        <div className="button-container">
                                            {["before", "after", "same"].map((category) => (
                                                <Button
                                                    key={category}
                                                    className={`dashboard-button ${activeCategory === category ? 'active' : ''}`}
                                                    onClick={() => handleCategoryChange(category)}
                                                >
                                                    {category.toUpperCase()}
                                                </Button>
                                            ))}
                                        </div>
                                    </Card.Body>
                                </Card>
                            </Col>

                            {/* Maintenance Details */}
                            <Col md={6} className="card-item">
                                <Card className="shadow-sm card-full-height nested-card">
                                    <Card.Body className="py-2 px-3">
                                        {experimentInfo ? (
                                            <Row>
                                                <Col md={6}>
                                                    <p className="mb-1">
                                                        <strong>Date Difference:</strong> <br />
                                                        {experimentInfo.date_diff}
                                                    </p>
                                                    <p className="mb-1">
                                                        <strong>Flight Length:</strong> {experimentInfo.flight_length} hrs
                                                    </p>
                                                </Col>
                                                <Col md={6}>
                                                    <p className="mb-1">
                                                        <strong>Issue:</strong> {experimentInfo.label}
                                                    </p>
                                                    <p className="mb-1">
                                                        <strong>Number of Flights Before:</strong> {experimentInfo.number_flights_before}
                                                    </p>
                                                </Col>
                                            </Row>
                                        ) : (
                                            <p>No event selected. Details will appear here.</p>
                                        )}
                                    </Card.Body>
                                </Card>
                            </Col>
                        </Row>
                    </Card.Body>
                </Card>

                {/* Loading Spinner */}
                {loading && (
                    <Row className="mb-3">
                        <Col className="text-center">
                            <Spinner animation="border" variant="light" />
                        </Col>
                    </Row>
                )}

                {/* Error Alert */}
                {error && (
                    <Row className="mb-3">
                        <Col>
                            <Alert variant="danger">{error}</Alert>
                        </Col>
                    </Row>
                )}

                {/* Maintenance Data Visualization Section */}
                {maintenanceData && (
                    <Card className="shadow-lg section-padding card-padding">
                        <Card.Body>
                            <h4 className="text-center mb-4" style={{ fontWeight: "bold" }}>
                                Maintenance Data Visualizations
                            </h4>
                            <Row>
                                {/* Flight Length vs Date Difference Chart */}
                                <Col md={12} className="mb-3">
                                    <Card className="shadow-sm h-100 nested-card">
                                        <Card.Header className="py-2">Flight Length vs Date Difference</Card.Header>
                                        <Card.Body className="p-2">
                                            {renderMaintenanceChart()}
                                        </Card.Body>
                                    </Card>
                                </Col>
                                {/* Additional charts can be added here */}
                            </Row>
                        </Card.Body>
                    </Card>
                )}
            </Container>
        </div>
    );
};

export default NGAFIDDashboard; // Ensure correct export
