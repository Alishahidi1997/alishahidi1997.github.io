import React from 'react';


function Icons(props){
    const iconSize = 28; 
  return (
    <a href={props.link} style={{ color: 'gray', textDecoration: 'none' }} target="_blank" rel="noopener noreferrer" className="text-decoration-none">
      <props.icon className="m-2" size={iconSize} />
    </a>
  );
};

export default Icons;