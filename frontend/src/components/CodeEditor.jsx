import React from 'react';

const CodeEditor = ({ title, language, setLanguage, code, setCode, onClear }) => {
  return (
    <div className="flex flex-col h-full bg-slate-800 rounded-lg border border-slate-700 overflow-hidden">
      <div className="flex justify-between items-center bg-slate-900 px-4 py-2 border-b border-slate-700">
        <h3 className="font-semibold text-slate-300">{title}</h3>
        <div className="flex items-center gap-3">
          <select 
            value={language} 
            onChange={(e) => setLanguage(e.target.value)}
            className="bg-slate-700 text-sm text-white px-2 py-1 rounded outline-none border border-slate-600 focus:border-blue-500"
          >
            <option value="python">Python</option>
            <option value="javascript">JavaScript</option>
          </select>
          <button 
            onClick={onClear}
            className="text-xs text-slate-400 hover:text-red-400 transition-colors"
          >
            Clear
          </button>
        </div>
      </div>
      <textarea
        value={code}
        onChange={(e) => setCode(e.target.value)}
        className="flex-1 w-full p-4 bg-slate-800 text-slate-200 font-mono text-sm resize-none outline-none focus:ring-1 focus:ring-blue-500/50"
        placeholder={`Paste ${language} code here...`}
        spellCheck="false"
      />
    </div>
  );
};

export default CodeEditor;
