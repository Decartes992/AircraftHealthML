// frontend/src/components/LandingPage.jsx

import React from 'react';
import { Container, Row, Col, Card, Button } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { Activity, Database, LineChart } from 'lucide-react';

const LandingPage = () => {
    return (
        <div className="min-h-screen bg-gray-50">
            {/* Hero Section */}
            <div className="bg-primary text-white py-5">
                <Container>
                    <Row className="align-items-center py-5">
                        <Col md={6}>
                            <h1 className="display-4 fw-bold">Aircraft Health Monitoring</h1>
                            <p className="lead mb-4">
                                Advanced diagnostics and prognostics for aerospace systems using machine learning
                            </p>
                            <Link to="/dashboard">
                                <Button variant="light" size="lg">
                                    View Dashboard
                                </Button>
                            </Link>
                        </Col>
                        <Col md={6} className="text-center">
                            <LineChart size={300} className="text-white" />
                        </Col>
                    </Row>
                </Container>
            </div>

            {/* Features Section */}
            <Container className="py-5">
                <h2 className="text-center mb-5">Key Features</h2>
                <Row>
                    <Col md={4} className="mb-4">
                        <Card className="h-100 shadow-sm">
                            <Card.Body className="text-center">
                                <Activity size={40} className="text-primary mb-3" />
                                <Card.Title>Real-time Monitoring</Card.Title>
                                <Card.Text>
                                    Monitor critical aircraft systems in real-time with advanced sensor data analysis
                                </Card.Text>
                            </Card.Body>
                        </Card>
                    </Col>
                    <Col md={4} className="mb-4">
                        <Card className="h-100 shadow-sm">
                            <Card.Body className="text-center">
                                <Database size={40} className="text-primary mb-3" />
                                <Card.Title>Predictive Maintenance</Card.Title>
                                <Card.Text>
                                    Predict potential failures before they occur using machine learning algorithms
                                </Card.Text>
                            </Card.Body>
                        </Card>
                    </Col>
                    <Col md={4} className="mb-4">
                        <Card className="h-100 shadow-sm">
                            <Card.Body className="text-center">
                                <LineChart size={40} className="text-primary mb-3" />
                                <Card.Title>Component Analysis</Card.Title>
                                <Card.Text>
                                    Analyze component interactions and identify potential cascading failures
                                </Card.Text>
                            </Card.Body>
                        </Card>
                    </Col>
                </Row>
            </Container>

            {/* Dataset Section */}
            <div className="bg-light py-5">
                <Container>
                    <Row className="align-items-center">
                        <Col md={6}>
                            <h2>ADAPT Dataset</h2>
                            <p className="lead">
                                Using NASA's Advanced Diagnostics and Prognostics Testbed (ADAPT) for high-fidelity analysis
                            </p>
                            <Link to="/dashboard">
                                <Button variant="primary">Explore Data</Button>
                            </Link>
                        </Col>
                        <Col md={6} className="text-center">
                            <Database size={200} className="text-primary" />
                        </Col>
                    </Row>
                </Container>
            </div>
        </div>
    );
};

export default LandingPage;