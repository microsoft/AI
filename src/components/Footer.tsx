import React from 'react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-slate-200">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="mt-8 md:order-1 md:mt-0">
          <p className="text-center text-xs leading-5 text-slate-500">
            &copy; {new Date().getFullYear()} Microsoft AI Open Source Collection. All rights reserved.
          </p>
          <p className="text-center text-xs leading-5 text-slate-400 mt-2">
            This portal is a frontend contribution to improve the accessibility of the Microsoft AI repository.
          </p>
        </div>
      </div>
    </footer>
  );
};
