import { useState } from 'react';
import { Shield, ShieldAlert, Globe, Clock, MapPin, Activity, ChevronRight, Loader2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function App() {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const analyzeUrl = async (e) => {
    e.preventDefault();
    if (!url) return;

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response = await fetch('http://localhost:10000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });

      if (!response.ok) {
        throw new Error('Analysis failed. Ensure the backend is running.');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen p-6 md:p-12 relative overflow-hidden">
      
      {/* Background decorations */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-cyber-blue/10 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-purple-600/10 blur-[120px] pointer-events-none" />

      <main className="max-w-5xl mx-auto relative z-10">
        
        {/* Header */}
        <header className="mb-16 text-center space-y-4">
          <motion.div 
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="inline-flex items-center justify-center p-4 rounded-2xl bg-white/5 border border-white/10 mb-4"
          >
            <Shield className="w-10 h-10 text-cyber-blue" />
          </motion.div>
          <h1 className="text-5xl md:text-6xl font-extrabold font-outfit tracking-tight text-transparent bg-clip-text bg-gradient-to-r from-white to-gray-400">
            PhishGuard <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyber-blue to-purple-500">AI</span>
          </h1>
          <p className="text-gray-400 text-lg max-w-2xl mx-auto font-light">
            Advanced Machine Learning threat intelligence pipeline. Analyze URLs in real-time to detect phishing vectors with SHAP explainability.
          </p>
        </header>

        {/* Input Form */}
        <motion.form 
          initial={{ y: 20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          onSubmit={analyzeUrl} 
          className="max-w-3xl mx-auto relative group"
        >
          <div className="absolute inset-0 bg-gradient-to-r from-cyber-blue to-purple-600 rounded-2xl blur opacity-25 group-hover:opacity-40 transition-opacity duration-500" />
          <div className="relative glass-panel p-2 flex items-center">
             <div className="pl-4 pr-2 text-gray-400">
                <Globe className="w-6 h-6" />
             </div>
             <input
                type="url"
                required
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Enter URL to analyze (e.g., https://example.com)..."
                className="flex-1 bg-transparent border-none text-white outline-none placeholder:text-gray-500 py-4 px-2 text-lg font-mono"
             />
             <button
                type="submit"
                disabled={loading}
                className="bg-white/10 hover:bg-white/20 border border-white/10 text-white px-8 py-4 rounded-xl font-medium tracking-wide transition-all duration-300 disabled:opacity-50 flex items-center space-x-2"
             >
                {loading ? <Loader2 className="w-5 h-5 animate-spin" /> : <span>Analyze</span>}
             </button>
          </div>
        </motion.form>

        {error && (
            <div className="mt-8 max-w-3xl mx-auto text-red-400 bg-red-400/10 border border-red-400/20 p-4 rounded-xl text-center">
              {error}
            </div>
        )}

        <AnimatePresence>
          {result && !loading && (
            <motion.div 
              initial={{ y: 30, opacity: 0 }}
              animate={{ y: 0, opacity: 1 }}
              exit={{ y: -20, opacity: 0 }}
              className="mt-16 grid grid-cols-1 lg:grid-cols-3 gap-6 max-w-5xl mx-auto"
            >
              
              {/* Main Prediction Card */}
              <div className="col-span-1 lg:col-span-1 glass-panel p-8 flex flex-col items-center justify-center text-center space-y-6 relative overflow-hidden">
                {result.prediction === 'Phishing' ? (
                  <div className="absolute inset-0 bg-red-500/10 animate-pulse-slow" />
                ) : (
                  <div className="absolute inset-0 bg-green-500/10 animate-pulse-slow" />
                )}
                
                <div className={`relative z-10 p-6 rounded-full border-2 ${result.prediction === 'Phishing' ? 'border-red-500 text-red-500 bg-red-500/10' : 'border-green-500 text-green-500 bg-green-500/10'}`}>
                   {result.prediction === 'Phishing' ? <ShieldAlert className="w-16 h-16" /> : <Shield className="w-16 h-16" />}
                </div>
                
                <div className="relative z-10">
                  <h2 className="text-3xl font-bold font-outfit uppercase tracking-wider mb-2">
                    {result.prediction}
                  </h2>
                  <div className="flex items-center justify-center space-x-2 text-gray-400 font-mono text-sm">
                    <Activity className="w-4 h-4" />
                    <span>Confidence: {(result.probability * 100).toFixed(1)}%</span>
                  </div>
                </div>
              </div>

              {/* Threat Intelligence */}
              <div className="col-span-1 lg:col-span-1 flex flex-col space-y-6">
                <div className="glass-panel p-6 flex-1 flex flex-col justify-center">
                  <h3 className="text-gray-400 text-sm font-semibold uppercase tracking-wider mb-4 flex items-center">
                    <MapPin className="w-4 h-4 mr-2" /> Geolocation
                  </h3>
                  <div className="text-2xl font-outfit font-medium">
                    {result.location.city}, <span className="text-gray-300">{result.location.country}</span>
                  </div>
                </div>

                <div className="glass-panel p-6 flex-1 flex flex-col justify-center">
                  <h3 className="text-gray-400 text-sm font-semibold uppercase tracking-wider mb-4 flex items-center">
                    <Clock className="w-4 h-4 mr-2" /> Domain Age
                  </h3>
                  <div className="text-3xl font-outfit font-medium text-cyber-blue">
                    {result.domain_age < 0 ? 'Unknown' : `${result.domain_age} days`}
                  </div>
                </div>
              </div>

              {/* SHAP Explanation */}
              <div className="col-span-1 lg:col-span-1 glass-panel p-6">
                <h3 className="text-gray-400 text-sm font-semibold uppercase tracking-wider mb-6 flex items-center">
                   <Activity className="w-4 h-4 mr-2" /> ML Explanation
                </h3>
                <ul className="space-y-4">
                  {result.explanation.map((exp, idx) => (
                    <li key={idx} className="flex items-start space-x-3 text-sm">
                      <ChevronRight className="w-5 h-5 text-cyber-blue flex-shrink-0 mt-0.5" />
                      <span className="text-gray-300 leading-relaxed font-light">{exp}</span>
                    </li>
                  ))}
                </ul>
              </div>

            </motion.div>
          )}
        </AnimatePresence>
      </main>

    </div>
  );
}
