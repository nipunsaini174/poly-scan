import React from 'react';
import ActionTags from './ActionTags';
import BehaviorGraph from './BehaviorGraph';

const AnalysisResult = ({ result }) => {
  if (!result) return null;

  const { similarity, tags_a, tags_b, graph_a, graph_b, language_a, language_b } = result;

  return (
    <div className="mt-6 flex flex-col gap-6">
      <div className="bg-slate-800 border border-slate-700 p-6 rounded-lg shadow-lg">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-6">
          <div>
            <h2 className="text-xl font-bold text-white mb-1">Behavioral Similarity Analysis</h2>
            <p className="text-slate-400 text-sm">{similarity.explanation}</p>
          </div>
          <div className="mt-4 md:mt-0 flex items-center bg-slate-900 px-4 py-3 rounded-lg border border-slate-700">
            <span className="text-sm text-slate-400 mr-3">Similarity:</span>
            <span className={`text-3xl font-bold ${similarity.similarity_percentage > 80 ? 'text-rose-500' : similarity.similarity_percentage > 40 ? 'text-amber-500' : 'text-emerald-500'}`}>
              {similarity.similarity_percentage}%
            </span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-slate-300 border-b border-slate-700 pb-2">Code A ({language_a})</h3>
            <ActionTags title="Extracted Tags" tags={tags_a} />
            <div>
              <h4 className="text-sm font-medium text-slate-400 mb-2">Behavior Graph</h4>
              <BehaviorGraph graphData={graph_a} />
            </div>
          </div>
          <div className="space-y-4">
            <h3 className="text-lg font-semibold text-slate-300 border-b border-slate-700 pb-2">Code B ({language_b})</h3>
            <ActionTags title="Extracted Tags" tags={tags_b} />
            <div>
              <h4 className="text-sm font-medium text-slate-400 mb-2">Behavior Graph</h4>
              <BehaviorGraph graphData={graph_b} />
            </div>
          </div>
        </div>
      </div>

      <div className="bg-slate-800 border border-slate-700 p-6 rounded-lg shadow-lg">
         <h3 className="text-lg font-semibold text-slate-300 mb-4">Comparison Breakdown</h3>
         <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
                <h4 className="text-sm font-medium text-emerald-400 mb-2">Matched Behaviors</h4>
                {similarity.matched_actions.length > 0 ? (
                    <ul className="space-y-1">
                        {similarity.matched_actions.map(a => (
                            <li key={a} className="text-sm text-slate-300 font-mono flex items-center before:content-['✓'] before:mr-2 before:text-emerald-500">{a}</li>
                        ))}
                    </ul>
                ) : <span className="text-sm text-slate-500">None</span>}
            </div>
            <div>
                <h4 className="text-sm font-medium text-blue-400 mb-2">Only in Code A</h4>
                {similarity.unique_to_a.length > 0 ? (
                    <ul className="space-y-1">
                        {similarity.unique_to_a.map(a => (
                            <li key={a} className="text-sm text-slate-300 font-mono flex items-center before:content-['→'] before:mr-2 before:text-blue-500">{a}</li>
                        ))}
                    </ul>
                ) : <span className="text-sm text-slate-500">None</span>}
            </div>
            <div>
                <h4 className="text-sm font-medium text-blue-400 mb-2">Only in Code B</h4>
                {similarity.unique_to_b.length > 0 ? (
                    <ul className="space-y-1">
                        {similarity.unique_to_b.map(a => (
                            <li key={a} className="text-sm text-slate-300 font-mono flex items-center before:content-['→'] before:mr-2 before:text-blue-500">{a}</li>
                        ))}
                    </ul>
                ) : <span className="text-sm text-slate-500">None</span>}
            </div>
         </div>
      </div>
    </div>
  );
};

export default AnalysisResult;
