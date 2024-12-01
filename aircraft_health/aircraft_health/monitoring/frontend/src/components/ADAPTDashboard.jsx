import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import Papa from 'papaparse';
import _ from 'lodash';

const ADAPTDashboard = () => {
  const [experiments, setExperiments] = useState([]);
  const [selectedExperiment, setSelectedExperiment] = useState(null);
  const [sensorData, setSensorData] = useState([]);
  const [faultInfo, setFaultInfo] = useState(null);

  useEffect(() => {
    const loadExperiment = async (filename) => {
      try {
        // Load sensor data
        const sensorResponse = await window.fs.readFile(`processed_${filename}.csv`);
        const sensorText = new TextDecoder().decode(sensorResponse);
        
        // Parse sensor data
        Papa.parse(sensorText, {
          header: true,
          dynamicTyping: true,
          complete: (results) => {
            setSensorData(results.data);
          }
        });

        // Load fault info
        const faultResponse = await window.fs.readFile(`fault_info_${filename}.csv`);
        const faultText = new TextDecoder().decode(faultResponse);
        
        // Parse fault info
        Papa.parse(faultText, {
          header: true,
          dynamicTyping: true,
          complete: (results) => {
            setFaultInfo(results.data[0]);
          }
        });
      } catch (error) {
        console.error('Error loading experiment:', error);
      }
    };

    // Load experiments when component mounts
    const loadExperiments = async () => {
      // You would need to implement this to get list of processed experiments
      const experimentFiles = ['Exp_304_comp3_pb.txt', 'Exp_305_comp3_pb.txt']; // Example
      setExperiments(experimentFiles);
    };

    loadExperiments();
  }, []);

  return (
    <div className="p-4 space-y-4">
      <Card>
        <CardHeader>
          <CardTitle>ADAPT Dataset Visualization</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {/* Experiment Selector */}
            <select 
              className="w-full p-2 border rounded"
              onChange={(e) => setSelectedExperiment(e.target.value)}
            >
              <option value="">Select Experiment</option>
              {experiments.map(exp => (
                <option key={exp} value={exp}>{exp}</option>
              ))}
            </select>

            {/* Fault Information */}
            {faultInfo && (
              <Card>
                <CardHeader>
                  <CardTitle>Fault Information</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <strong>Component:</strong> {faultInfo.component}
                    </div>
                    <div>
                      <strong>Type:</strong> {faultInfo.type}
                    </div>
                    <div>
                      <strong>Location:</strong> {faultInfo.location}
                    </div>
                    <div>
                      <strong>Duration:</strong> {faultInfo.duration}s
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}

            {/* Sensor Data Visualization */}
            {sensorData.length > 0 && (
              <div className="h-96">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={sensorData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="Time" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    {Object.keys(sensorData[0])
                      .filter(key => key !== 'Time')
                      .map((sensor, idx) => (
                        <Line 
                          key={sensor}
                          type="monotone"
                          dataKey={sensor}
                          stroke={`hsl(${idx * 30}, 70%, 50%)`}
                          dot={false}
                        />
                      ))}
                  </LineChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ADAPTDashboard;