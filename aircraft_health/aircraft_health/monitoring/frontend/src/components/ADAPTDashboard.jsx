import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Form, Spinner, Alert } from 'react-bootstrap';
import { ResponsiveLine } from '@nivo/line';
import Papa from 'papaparse';

const ADAPTDashboard = () => {
    const [experiments, setExperiments] = useState([]);
    const [selectedExperiment, setSelectedExperiment] = useState(null);
    const [sensorData, setSensorData] = useState([]);
    const [faultInfo, setFaultInfo] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

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
                
                if (data.error) {
                    throw new Error(data.error);
                }

                // Parse sensor data
                const sensorData = Papa.parse(data.sensor_data, {
                    header: true,
                    dynamicTyping: true
                }).data;

                // Transform data for visualization
                const transformed = Object.keys(sensorData[0])
                    .filter(key => key !== 'Time')
                    .map(sensor => ({
                        id: sensor,
                        data: sensorData.map(d => ({
                            x: new Date(d.Time),
                            y: parseFloat(d[sensor])
                        }))
                    }));

                setSensorData(transformed);

                // Parse fault info
                const faultInfo = Papa.parse(data.fault_info, {
                    header: true,
                    dynamicTyping: true
                }).data[0];

                setFaultInfo(faultInfo);
                setLoading(false);
            } catch (error) {
                setError('Error loading experiment data');
                setLoading(false);
                console.error('Error details:', error);
            }
        };

        if (selectedExperiment) {
            loadExperiment(selectedExperiment);
        }
    }, [selectedExperiment]);

    return (
        <Container fluid className="p-4">
            {/* Header */}
            <Row className="mb-4">
                <Col>
                    <h1>ADAPT Dataset Dashboard</h1>
                </Col>
            </Row>

            {/* Experiment Selector */}
            <Row className="mb-4">
                <Col>
                    <Card>
                        <Card.Body>
                            <Form.Group>
                                <Form.Label>Select Experiment</Form.Label>
                                <Form.Control 
                                    as="select"
                                    value={selectedExperiment || ''}
                                    onChange={(e) => setSelectedExperiment(e.target.value)}
                                >
                                    <option value="">Choose an experiment...</option>
                                    {experiments.map(exp => (
                                        <option key={exp} value={exp}>{exp}</option>
                                    ))}
                                </Form.Control>
                            </Form.Group>
                        </Card.Body>
                    </Card>
                </Col>
            </Row>

            {/* Loading Spinner */}
            {loading && (
                <Row className="mb-4">
                    <Col className="text-center">
                        <Spinner animation="border" />
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

            {/* Fault Information */}
            {faultInfo && (
                <Row className="mb-4">
                    <Col>
                        <Card>
                            <Card.Header>
                                <h5 className="mb-0">Fault Information</h5>
                            </Card.Header>
                            <Card.Body>
                                <Row>
                                    <Col md={3}>
                                        <strong>Component:</strong> {faultInfo.component}
                                    </Col>
                                    <Col md={3}>
                                        <strong>Type:</strong> {faultInfo.type}
                                    </Col>
                                    <Col md={3}>
                                        <strong>Location:</strong> {faultInfo.location}
                                    </Col>
                                    <Col md={3}>
                                        <strong>Duration:</strong> {faultInfo.duration}s
                                    </Col>
                                </Row>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            )}

            {/* Sensor Data Visualization */}
            {sensorData.length > 0 && (
                <Row>
                    <Col>
                        <Card>
                            <Card.Header>
                                <h5 className="mb-0">Sensor Data</h5>
                            </Card.Header>
                            <Card.Body>
                                <div style={{ height: '500px' }}>
                                    <ResponsiveLine
                                        data={sensorData}
                                        margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
                                        xScale={{
                                            type: 'time',
                                            format: '%Y-%m-%d %H:%M:%S.%L',
                                            useUTC: false,
                                            precision: 'millisecond'
                                        }}
                                        xFormat="time:%Y-%m-%d %H:%M:%S.%L"
                                        yScale={{
                                            type: 'linear',
                                            stacked: false,
                                        }}
                                        axisLeft={{
                                            legend: 'Sensor Values',
                                            legendOffset: -40,
                                            legendPosition: 'middle'
                                        }}
                                        axisBottom={{
                                            format: '%H:%M:%S',
                                            legend: 'Time',
                                            legendOffset: 36,
                                            legendPosition: 'middle'
                                        }}
                                        pointSize={0}
                                        lineWidth={1}
                                        enablePoints={false}
                                        enableGridX={true}
                                        enableGridY={true}
                                        enableCrosshair={true}
                                        useMesh={true}
                                        legends={[
                                            {
                                                anchor: 'bottom-right',
                                                direction: 'column',
                                                justify: false,
                                                translateX: 100,
                                                translateY: 0,
                                                itemsSpacing: 0,
                                                itemDirection: 'left-to-right',
                                                itemWidth: 80,
                                                itemHeight: 20,
                                                itemOpacity: 0.75,
                                                symbolSize: 12,
                                                symbolShape: 'circle'
                                            }
                                        ]}
                                    />
                                </div>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            )}
        </Container>
    );
};

export default ADAPTDashboard;