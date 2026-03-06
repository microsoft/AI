import React from 'react';

const FOOTER_SECTIONS = [
  {
    heading: 'Explore',
    links: [
      { label: 'AI100 - Samples', href: '#ai100' },
      { label: 'AI200 - Architectures', href: '#ai200' },
      { label: 'AI300 - Best Practices', href: '#ai300' },
    ],
  },
  {
    heading: 'Resources',
    links: [
      { label: 'ML For Beginners', href: 'https://github.com/microsoft/ML-For-Beginners' },
      { label: 'Azure ML Docs', href: 'https://docs.microsoft.com/en-us/azure/machine-learning/' },
      { label: 'Azure AI Services', href: 'https://azure.microsoft.com/en-us/products/ai-services/' },
    ],
  },
  {
    heading: 'Community',
    links: [
      { label: 'GitHub Repository', href: 'https://github.com/microsoft/ai' },
      { label: 'Contributing Guide', href: 'https://github.com/microsoft/ai/blob/master/CONTRIBUTING.md' },
      { label: 'Code of Conduct', href: 'https://opensource.microsoft.com/codeofconduct/' },
    ],
  },
];

export const Footer: React.FC = () => {
  return (
    <footer className="bg-slate-900 text-slate-300">
      <div className="mx-auto max-w-7xl px-4 py-12 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 gap-8 sm:grid-cols-3 mb-10">
          {FOOTER_SECTIONS.map(section => (
            <div key={section.heading}>
              <h3 className="text-sm font-semibold text-white tracking-wider uppercase mb-4">
                {section.heading}
              </h3>
              <ul className="space-y-2">
                {section.links.map(link => (
                  <li key={link.label}>
                    <a
                      href={link.href}
                      target={link.href.startsWith('http') ? '_blank' : undefined}
                      rel={link.href.startsWith('http') ? 'noopener noreferrer' : undefined}
                      className="text-sm hover:text-white transition-colors"
                    >
                      {link.label}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="border-t border-slate-700 pt-8">
          <p className="text-center text-xs leading-5 text-slate-500">
            &copy; {new Date().getFullYear()} Microsoft AI Open Source Collection. All rights reserved.
          </p>
          <p className="text-center text-xs leading-5 text-slate-600 mt-2">
            This portal is a frontend contribution to improve the accessibility of the Microsoft AI repository.
          </p>
        </div>
      </div>
    </footer>
  );
};
