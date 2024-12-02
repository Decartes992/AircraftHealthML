import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Form, Spinner, Alert, Nav } from 'react-bootstrap';
import { ResponsiveLine } from '@nivo/line';
import Papa from 'papaparse';

const ADAPTDashboard = () => {
    const [experiments, setExperiments] = useState([]);
    const [selectedExperiment, setSelectedExperiment] = useState(null);
    const [sensorData, setSensorData] = useState(null);
    const [experimentInfo, setExperimentInfo] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Helper function to parse experiment info from raw string
    const parseExperimentInfo = (rawInfo) => {
        try {
            // If rawInfo is already an object, just return formatted data
            if (rawInfo && typeof rawInfo === 'object' && !Array.isArray(rawInfo)) {
                return {
                    startTime: rawInfo.startTime || '',
                    endTime: rawInfo.endTime || '',
                    operationCode: rawInfo.operationCode || '',
                    operationMode: rawInfo.operationMode || '',
                    testArticle: rawInfo.testArticle || '',
                    comments: rawInfo.comments || '',
                    faultType: rawInfo.faultType || '',
                    faultMode: rawInfo.faultMode || '',
                    faultLocation: rawInfo.faultLocation || '',
                    faultInjection: rawInfo.faultInjection || ''
                };
            }
            
            return {
                startTime: '',
                endTime: '',
                operationCode: rawInfo?.operationCode || '',
                operationMode: '',
                testArticle: '',
                comments: '',
                faultType: rawInfo?.faultType || '',
                faultMode: rawInfo?.faultMode || '',
                faultLocation: rawInfo?.faultLocation || '',
                faultInjection: ''
            };
        } catch (error) {
            console.error('Error parsing experiment info:', error);
            return {
                startTime: '',
                endTime: '',
                operationCode: '',
                operationMode: '',
                testArticle: '',
                comments: '',
                faultType: '',
                faultMode: '',
                faultLocation: '',
                faultInjection: ''
            };
        }
    };

    // Load experiment list
    useEffect(() => {
        const loadExperiments = async () => {
            try {
                const response = await fetch('/api/experiments/');
                const data = await response.json();
                
                if (data.error) {
                    throw new Error(data.error);
                }
                
                console.log('Found experiments:', data.experiments);
                setExperiments(data.experiments);
            } catch (error) {
                console.error('Error loading experiment list:', error);
                setError('Failed to load experiment list');
            }
        };

        loadExperiments();
    }, []);

    // Load experiment data when selection changes
    useEffect(() => {
        const loadExperiment = async (filename) => {
            try {
                setLoading(true);
                setError(null);

                const response = await fetch(`/api/experiments/${filename}/`);
                const data = await response.json();
                
                console.log('Raw API response:', data);

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                // Process experiment info
                if (data.experiment_info) {
                    const expInfo = parseExperimentInfo(data.experiment_info);
                    setExperimentInfo(expInfo);
                } else {
                    console.warn('No experiment_info found in data:', data);
                }

                // Process sensor data
                if (data.sensor_data && Array.isArray(data.sensor_data)) {
                    const sensorDataByType = processNewSensorData(data.sensor_data);
                    setSensorData(sensorDataByType);
                }

                setLoading(false);
            } catch (error) {
                console.error('Detailed error:', {
                    message: error.message,
                    stack: error.stack,
                    error: error
                });
                setError(`Error loading experiment data: ${error.message}`);
                setLoading(false);
            }
        };

        if (selectedExperiment) {
            loadExperiment(selectedExperiment);
        }
    }, [selectedExperiment]);

    // Add this new function to process sensor data
    const processNewSensorData = (sensorData) => {
        const sensorDataByType = {
            voltage: {},
            current: {},
            temp: {},
            flow: {},
            load: {},
            status: {},
            relay: {}
        };

        sensorData.forEach(row => {
            if (row.SensorData === 'AntagonistData') {
                const time = new Date(row.Time);
                Object.entries(row).forEach(([key, value]) => {
                    if (key !== 'Time' && key !== 'SensorData') {
                        // Determine sensor type and store data
                        if (key.startsWith('E') && !key.startsWith('ESH')) {
                            if (!sensorDataByType.voltage[key]) sensorDataByType.voltage[key] = [];
                            sensorDataByType.voltage[key].push({ x: time, y: parseFloat(value) });
                        } else if (key.startsWith('ISH')) {
                            if (!sensorDataByType.current[key]) sensorDataByType.current[key] = [];
                            sensorDataByType.current[key].push({ x: time, y: parseFloat(value) });
                        } else if (key.startsWith('ESH')) {
                            if (!sensorDataByType.relay[key]) sensorDataByType.relay[key] = [];
                            sensorDataByType.relay[key].push({ x: time, y: parseFloat(value) });
                        } else if (key.startsWith('IT') || key.startsWith('TE')) {
                            if (!sensorDataByType.temp[key]) sensorDataByType.temp[key] = [];
                            sensorDataByType.temp[key].push({ x: time, y: parseFloat(value) });
                        } else if (key.startsWith('FT')) {
                            if (!sensorDataByType.flow[key]) sensorDataByType.flow[key] = [];
                            sensorDataByType.flow[key].push({ x: time, y: parseFloat(value) });
                        } else if (key.startsWith('LT')) {
                            if (!sensorDataByType.load[key]) sensorDataByType.load[key] = [];
                            sensorDataByType.load[key].push({ x: time, y: parseFloat(value) });
                        } else if (key.startsWith('ST')) {
                            if (!sensorDataByType.status[key]) sensorDataByType.status[key] = [];
                            sensorDataByType.status[key].push({ x: time, y: parseFloat(value) });
                        }
                    }
                });
            }
        });

        return sensorDataByType;
    };

    const renderSensorChart = (data, title, yAxisLabel, height = '300px') => {
        if (!data || Object.keys(data).length === 0) {
            return <div className="text-white text-center">No data available</div>;
        }
    
        const chartData = Object.entries(data).map(([sensor, values]) => ({
            id: sensor,
            data: values
        }));
    
        return (
            <div style={{ height: height }} className="chart-container">
                <ResponsiveLine
                    data={chartData}
                    margin={{ top: 20, right: 120, bottom: 40, left: 50 }}
                    xScale={{
                        type: 'time',
                        format: 'time',
                        useUTC: false,
                        precision: 'second'
                    }}
                    yScale={{
                        type: 'linear',
                        stacked: false,
                        min: 'auto',
                        max: 'auto',
                    }}
                    axisLeft={{
                        legend: yAxisLabel,
                        legendOffset: -40,
                        legendPosition: 'middle',
                        textColor: '#ffffff'
                    }}
                    axisBottom={{
                        format: '%H:%M:%S',
                        legend: 'Time',
                        legendOffset: 35,
                        legendPosition: 'middle',
                        tickRotation: -45,
                        textColor: '#ffffff'
                    }}
                    enablePoints={false}
                    enableGridX={true}
                    enableGridY={true}
                    enableCrosshair={true}
                    useMesh={true}
                    animate={false}
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
                    legends={[
                        {
                            anchor: 'right',
                            direction: 'column',
                            justify: false,
                            translateX: 100,
                            translateY: 0,
                            itemsSpacing: 2,
                            itemDirection: 'left-to-right',
                            itemWidth: 100,
                            itemHeight: 20,
                            itemOpacity: 0.85,
                            symbolSize: 12,
                            symbolShape: 'circle'
                        }
                    ]}
                />
            </div>
        );
    };

    return (
        <div className="min-h-screen bg-gray-900 text-white">
            <Container fluid className="p-4">
                {/* Header */}
                <Row className="mb-4">
                    <Col>
                        <h1 className="text-2xl font-bold">ADAPT Dataset Dashboard</h1>
                    </Col>
                </Row>

                {/* Experiment Selector */}
                <Row className="mb-4">
                    <Col>
                        <Card className="bg-gray-800 border-gray-700">
                            <Card.Body>
                                <Form.Group>
                                    <Form.Label className="text-white">Select Experiment</Form.Label>
                                    <Form.Select 
                                        value={selectedExperiment || ''}
                                        onChange={(e) => setSelectedExperiment(e.target.value)}
                                        className="bg-gray-700 text-white border-gray-600"
                                    >
                                        <option value="">Choose an experiment...</option>
                                        {experiments.map(exp => (
                                            <option key={exp} value={exp}>{exp}</option>
                                        ))}
                                    </Form.Select>
                                </Form.Group>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>

                {/* Loading Spinner */}
                {loading && (
                    <Row className="mb-4">
                        <Col className="text-center">
                            <Spinner animation="border" variant="light" />
                        </Col>
                    </Row>
                )}

                {/* Error Alert */}
                {error && (
                    <Row className="mb-4">
                        <Col>
                            <Alert variant="danger">{error}</Alert>
                        </Col>
                    </Row>
                )}

                {/* Experiment Info */}
                {experimentInfo && (
                    <Row className="mb-4">
                        <Col>
                            <Card className="bg-gray-800 border-gray-700">
                                <Card.Header className="bg-gray-700 text-white">
                                    <h5 className="mb-0">Experiment Information</h5>
                                </Card.Header>
                                <Card.Body className="text-white">
                                    <Row>
                                        <Col md={4}>
                                            <div className="mb-3">
                                                <strong>Time Period:</strong>
                                                <div>{experimentInfo.startTime} to {experimentInfo.endTime}</div>
                                            </div>
                                            <div className="mb-3">
                                                <strong>Operation:</strong>
                                                <div>Code: {experimentInfo.operationCode}</div>
                                                <div>Mode: {experimentInfo.operationMode}</div>
                                            </div>
                                        </Col>
                                        <Col md={4}>
                                            <div className="mb-3">
                                                <strong>Fault Information:</strong>
                                                <div>Type: {experimentInfo.faultType}</div>
                                                <div>Mode: {experimentInfo.faultMode}</div>
                                                <div>Location: {experimentInfo.faultLocation}</div>
                                                <div>Injection: {experimentInfo.faultInjection}</div>
                                            </div>
                                        </Col>
                                        <Col md={4}>
                                            <div className="mb-3">
                                                <strong>Test Article:</strong>
                                                <div>{experimentInfo.testArticle}</div>
                                            </div>
                                            <div className="mb-3">
                                                <strong>Comments:</strong>
                                                <div>{experimentInfo.comments}</div>
                                            </div>
                                        </Col>
                                    </Row>
                                </Card.Body>
                            </Card>
                        </Col>
                    </Row>
                )}

                {/* Sensor Data Grid */}
                {sensorData && (
                    <Row>
                        {/* Voltage Sensors */}
                        <Col md={6} className="mb-4">
                            <Card className="bg-gray-800 border-gray-700 h-100">
                                <Card.Header className="bg-gray-700 text-white">
                                    Voltage Sensors
                                </Card.Header>
                                <Card.Body>
                                    {renderSensorChart(sensorData.voltage, 'Voltage Sensors', 'Voltage (V)', '250px')}
                                </Card.Body>
                            </Card>
                        </Col>

                        {/* Current Sensors */}
                        <Col md={6} className="mb-4">
                            <Card className="bg-gray-800 border-gray-700 h-100">
                                <Card.Header className="bg-gray-700 text-white">
                                    Current Sensors
                                </Card.Header>
                                <Card.Body>
                                    {renderSensorChart(sensorData.current, 'Current Sensors', 'Current (A)', '250px')}
                                </Card.Body>
                            </Card>
                        </Col>

                        {/* Temperature Sensors */}
                        <Col md={6} className="mb-4">
                            <Card className="bg-gray-800 border-gray-700 h-100">
                                <Card.Header className="bg-gray-700 text-white">
                                    Temperature Sensors
                                </Card.Header>
                                <Card.Body>
                                    {renderSensorChart(sensorData.temp, 'Temperature Sensors', '°C', '250px')}
                                </Card.Body>
                            </Card>
                        </Col>

                        {/* Flow Rate Sensors */}
                        <Col md={6} className="mb-4">
                            <Card className="bg-gray-800 border-gray-700 h-100">
                                <Card.Header className="bg-gray-700 text-white">
                                    Flow Rate Sensors
                                </Card.Header>
                                <Card.Body>
                                    {renderSensorChart(sensorData.flow, 'Flow Rate Sensors', 'Flow Rate', '250px')}
                                </Card.Body>
                            </Card>
                        </Col>

                        {/* Relay Status */}
                        <Col md={6} className="mb-4">
                            <Card className="bg-gray-800 border-gray-700 h-100">
                                <Card.Header className="bg-gray-700 text-white">
                                    Relay Status
                                </Card.Header>
                                <Card.Body>
                                    {renderSensorChart(sensorData.relay, 'Relay Status', 'State', '250px')}
                                </Card.Body>
                            </Card>
                        </Col>

                        {/* Load Sensors */}
                        <Col md={6} className="mb-4">
                            <Card className="bg-gray-800 border-gray-700 h-100">
                                <Card.Header className="bg-gray-700 text-white">
                                    Load Sensors
                                </Card.Header>
                                <Card.Body>
                                    {renderSensorChart(sensorData.load, 'Load Sensors', 'Load', '250px')}
                                </Card.Body>
                            </Card>
                        </Col>

                        {/* Status Sensors - Full Width */}
                        <Col md={12}>
                            <Card className="bg-gray-800 border-gray-700">
                                <Card.Header className="bg-gray-700 text-white">
                                    Status Sensors
                                </Card.Header>
                                <Card.Body>
                                    {renderSensorChart(sensorData.status, 'Status Sensors', 'Status', '250px')}
                                </Card.Body>
                            </Card>
                        </Col>
                    </Row>
                )}
            </Container>
        </div>
    );
};

export default ADAPTDashboard;