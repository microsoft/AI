import React from 'react';
import { ResourceCategory } from '../data/resources';
import { ExternalLink } from 'lucide-react';
import { motion } from 'framer-motion';

interface Props {
  category: ResourceCategory;
  index: number;
}

export const ResourceSection: React.FC<Props> = ({ category, index }) => {
  const isEven = index % 2 === 0;
  
  return (
    <section id={category.id} className={`py-16 ${isEven ? 'bg-slate-50' : 'bg-white'}`}>
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="mb-12 max-w-2xl">
          <h2 className="text-3xl font-bold tracking-tight text-slate-900 sm:text-4xl">{category.title}</h2>
          <p className="mt-4 text-lg text-slate-600">{category.description}</p>
        </div>

        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {category.items.map((item, itemIndex) => {
            const Icon = item.icon;
            return (
              <motion.a
                key={item.id}
                href={item.url}
                target="_blank"
                rel="noopener noreferrer"
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.4, delay: itemIndex * 0.1 }}
                className="group relative flex flex-col overflow-hidden rounded-2xl bg-white p-6 shadow-sm ring-1 ring-slate-200 transition-all hover:shadow-md hover:ring-blue-200"
              >
                <div className="mb-4 flex h-10 w-10 items-center justify-center rounded-lg bg-blue-50 text-blue-600 group-hover:bg-blue-600 group-hover:text-white transition-colors">
                  {Icon && <Icon className="h-6 w-6" />}
                </div>
                
                <h3 className="mb-2 text-lg font-semibold text-slate-900 group-hover:text-blue-600 transition-colors">
                  {item.title}
                </h3>
                
                <p className="mb-4 flex-grow text-sm text-slate-600">
                  {item.description}
                </p>
                
                <div className="flex flex-wrap gap-2 mt-auto">
                  {item.tags.map(tag => (
                    <span key={tag} className="inline-flex items-center rounded-full bg-slate-100 px-2.5 py-0.5 text-xs font-medium text-slate-800">
                      {tag}
                    </span>
                  ))}
                </div>
                
                <div className="absolute top-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity text-slate-400">
                  <ExternalLink className="h-5 w-5" />
                </div>
              </motion.a>
            );
          })}
        </div>
      </div>
    </section>
  );
};
