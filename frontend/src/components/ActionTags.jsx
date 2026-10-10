import React from 'react';

const ActionTags = ({ tags, title }) => {
  if (!tags || tags.length === 0) {
    return (
      <div className="mb-4">
        <h4 className="text-sm font-medium text-slate-400 mb-2">{title}</h4>
        <p className="text-xs text-slate-500 italic">No recognizable behaviors extracted.</p>
      </div>
    );
  }

  return (
    <div className="mb-4">
      <h4 className="text-sm font-medium text-slate-400 mb-2">{title}</h4>
      <div className="flex flex-wrap gap-2">
        {tags.map((tag, idx) => (
          <span 
            key={idx} 
            className="px-2 py-1 bg-blue-900/40 text-blue-300 border border-blue-800/60 rounded text-xs font-mono"
            title={tag}
          >
            [{tag}]
          </span>
        ))}
      </div>
    </div>
  );
};

export default ActionTags;
