import React from 'react';
import { Github, Menu } from 'lucide-react';

export const Navbar: React.FC = () => {
  return (
    <nav className="sticky top-0 z-50 w-full border-b border-slate-200 bg-white/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-2">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-600 text-white font-bold">
            AI
          </div>
          <span className="text-lg font-semibold text-slate-900 hidden sm:block">Microsoft AI Open Source</span>
        </div>
        
        <div className="flex items-center gap-4">
          <a 
            href="https://github.com/microsoft/ai" 
            target="_blank" 
            rel="noopener noreferrer"
            className="flex items-center gap-2 rounded-md px-3 py-2 text-sm font-medium text-slate-700 hover:bg-slate-100 transition-colors"
          >
            <Github className="h-5 w-5" />
            <span className="hidden sm:inline">View on GitHub</span>
          </a>
          <button className="sm:hidden p-2 text-slate-600">
            <Menu className="h-6 w-6" />
          </button>
        </div>
      </div>
    </nav>
  );
};
