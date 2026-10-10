import React, { useMemo } from 'react';
import { ReactFlow, Background, Controls, MiniMap } from '@xyflow/react';
import '@xyflow/react/dist/style.css';

const BehaviorGraph = ({ graphData }) => {
  const { nodes, edges } = useMemo(() => {
    if (!graphData || !graphData.nodes) return { nodes: [], edges: [] };

    const flowNodes = graphData.nodes.map((node, i) => ({
      id: node.id.toString(),
      data: { label: node.action_type },
      position: { x: 150, y: i * 80 + 50 },
      style: {
        background: '#1e293b',
        color: '#93c5fd',
        border: '1px solid #3b82f6',
        borderRadius: '6px',
        fontSize: '12px',
        fontFamily: 'monospace',
        padding: '10px'
      }
    }));

    const flowEdges = (graphData.edges || []).map((edge, i) => ({
      id: `e${edge.source}-${edge.target}`,
      source: edge.source.toString(),
      target: edge.target.toString(),
      animated: true,
      style: { stroke: '#475569' }
    }));

    return { nodes: flowNodes, edges: flowEdges };
  }, [graphData]);

  if (nodes.length === 0) {
    return (
      <div className="h-48 w-full flex items-center justify-center bg-slate-900/50 rounded border border-slate-800">
        <span className="text-sm text-slate-500 italic">No graph data available</span>
      </div>
    );
  }

  return (
    <div className="h-64 w-full bg-slate-900 rounded border border-slate-700">
      <ReactFlow nodes={nodes} edges={edges} fitView>
        <Background color="#334155" gap={16} size={1} />
      </ReactFlow>
    </div>
  );
};

export default BehaviorGraph;
