import React from 'react';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { ResourceSection } from './components/ResourceSection';
import { Footer } from './components/Footer';
import { resources } from './data/resources';

function App() {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Navbar />
      <main className="flex-grow">
        <Hero />
        <div className="space-y-0">
          {resources.map((category, index) => (
            <ResourceSection 
              key={category.id} 
              category={category} 
              index={index} 
            />
          ))}
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default App;
