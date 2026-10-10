import React, { useState, useEffect, useRef } from 'react';
import { Activity, ShieldAlert, CheckCircle2, XCircle, Loader2 } from 'lucide-react';
import CodeEditor from '../components/CodeEditor';
import AnalysisResult from '../components/AnalysisResult';
import { PolyScanService } from '../services/websocket';

const Dashboard = () => {
  const [codeA, setCodeA] = useState('import os\nos.system("malware.exe")\nopen("x.txt", "w")');
  const [langA, setLangA] = useState('python');
  
  const [codeB, setCodeB] = useState('const cp = require("child_process");\ncp.exec("malware.exe");\nconst fs = require("fs");\nfs.writeFileSync("x.txt", "data");');
  const [langB, setLangB] = useState('javascript');

  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [stages, setStages] = useState([]);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const wsRef = useRef(null);

  const isAnalyzingRef = useRef(isAnalyzing);
  useEffect(() => {
    isAnalyzingRef.current = isAnalyzing;
  }, [isAnalyzing]);

  useEffect(() => {
    wsRef.current = new PolyScanService(
      (data) => {
        if (data.error) {
          setError(data.error);
          setIsAnalyzing(false);
        } else if (data.stage) {
          setStages(prev => [...prev, data.stage]);
        } else if (data.result) {
          setResult(data.result);
          setIsAnalyzing(false);
        }
      },
      (err) => {
        setError("WebSocket connection failed. Ensure backend is running.");
        setIsAnalyzing(false);
      },
      () => {
        if (isAnalyzingRef.current) {
          setError("WebSocket connection closed unexpectedly.");
          setIsAnalyzing(false);
        }
      }
    );
    return () => {
      wsRef.current.disconnect();
    };
  }, []);

  const handleAnalyze = () => {
    if (!codeA.trim() || !codeB.trim()) {
      setError("Both code inputs must be provided.");
      return;
    }
    setError(null);
    setResult(null);
    setStages([]);
    setIsAnalyzing(true);
    
    wsRef.current.analyze(codeA, langA, codeB, langB);
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 p-4 md:p-8">
      <header className="mb-8 flex items-center justify-between border-b border-slate-800 pb-4">
        <div className="flex items-center gap-3">
          <ShieldAlert className="text-blue-500 w-8 h-8" />
          <h1 className="text-2xl font-bold tracking-tight text-white">Poly-Scan</h1>
        </div>
        <div className="text-sm text-slate-500 font-mono hidden md:block">
          Static Cross-Language Behavioral Analysis
        </div>
      </header>

      <main className="max-w-7xl mx-auto space-y-6">
        
        {error && (
          <div className="bg-red-950/50 border border-red-900 text-red-200 p-4 rounded-lg flex items-start gap-3">
            <XCircle className="w-5 h-5 mt-0.5 shrink-0 text-red-500" />
            <div>
              <h3 className="font-semibold text-red-400">Analysis Error</h3>
              <p className="text-sm">{error}</p>
            </div>
          </div>
        )}

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 h-[400px]">
          <CodeEditor 
            title="Code A" 
            language={langA} 
            setLanguage={setLangA} 
            code={codeA} 
            setCode={setCodeA}
            onClear={() => setCodeA('')}
          />
          <CodeEditor 
            title="Code B" 
            language={langB} 
            setLanguage={setLangB} 
            code={codeB} 
            setCode={setCodeB}
            onClear={() => setCodeB('')}
          />
        </div>

        <div className="flex flex-col items-center justify-center py-4">
          <button
            onClick={handleAnalyze}
            disabled={isAnalyzing}
            className={`flex items-center gap-2 px-8 py-3 rounded-lg font-bold text-white transition-all shadow-lg ${
              isAnalyzing 
                ? 'bg-blue-800 cursor-not-allowed opacity-80' 
                : 'bg-blue-600 hover:bg-blue-500 hover:scale-105 active:scale-95 shadow-blue-900/20'
            }`}
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                ANALYZING...
              </>
            ) : (
              <>
                <Activity className="w-5 h-5" />
                ANALYZE BEHAVIOR
              </>
            )}
          </button>
        </div>

        {isAnalyzing && stages.length > 0 && (
          <div className="bg-slate-900 border border-slate-800 p-6 rounded-lg max-w-2xl mx-auto shadow-inner">
            <h3 className="text-sm font-semibold text-slate-400 mb-4 uppercase tracking-wider">Analysis Progress</h3>
            <ul className="space-y-3">
              {stages.map((stage, idx) => (
                <li key={idx} className="flex items-center gap-3 text-sm font-mono text-blue-300">
                  {idx === stages.length - 1 ? (
                    <Loader2 className="w-4 h-4 animate-spin text-blue-500" />
                  ) : (
                    <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                  )}
                  {stage}
                </li>
              ))}
            </ul>
          </div>
        )}

        {!isAnalyzing && result && (
          <AnalysisResult result={result} />
        )}
      </main>
    </div>
  );
};

export default Dashboard;
