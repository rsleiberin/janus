// Next.js: pages/index.js

import React, { useEffect, useState } from 'react';
import MainLayout from '../layouts/MainLayout';
import IntroOrganism from '../components/IntroOrganism';
import OrganismGrid from '../components/OrganismGrid';
import ProjectShowcase from '../components/ProjectShowcase';

const HomePage = () => {
  const [homeData, setHomeData] = useState({
    title: '',
    introText: '',
    projects: []
  });

  useEffect(() => {
    fetch('http://localhost:5000/')  // Replace with your Flask server URL
      .then(response => response.json())
      .then(data => setHomeData(data))
      .catch(error => console.error('Error fetching home data:', error));
  }, []);

  return (
    <MainLayout>
      <IntroOrganism
        title={homeData.title}
        description={homeData.introText}
        buttonText="Explore Projects"
      />
      <OrganismGrid>
        {homeData.projects.map(project => (
          <ProjectShowcase
            key={project.id}
            title={project.title}
            description={project.description}
            imageUrl="/path/to/image.jpg" // Replace with actual image path for each project
          />
        ))}
      </OrganismGrid>
      {/* Add more content or components that belong to the home page here */}
    </MainLayout>
  );
};

export default HomePage;
