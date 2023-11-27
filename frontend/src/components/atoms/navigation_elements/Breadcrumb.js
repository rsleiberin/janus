import React from 'react';
import { Link } from 'react-router-dom'; // Adjust based on your routing solution
import './breadcrumbsStyles.css'; // Link to your CSS file for Breadcrumbs

// Breadcrumbs Component
const Breadcrumbs = ({ breadcrumbItems }) => {
    return (
        <nav aria-label="breadcrumb">
            <ol className="breadcrumb">
                {breadcrumbItems.map((item, index) => (
                    <li key={index} className={`breadcrumb-item ${item.active ? 'active' : ''}`}>
                        {item.active ? item.label : <Link to={item.path}>{item.label}</Link>}
                    </li>
                ))}
            </ol>
        </nav>
    );
};

export default Breadcrumbs;

// Notes:
// - This component displays a breadcrumb trail.
// - 'breadcrumbItems' is an array of objects containing 'label', 'path', and 'active' properties.
// - The last item, representing the current page, is marked active and is not a link.
// - Uses semantic HTML for accessibility and is styled through an external CSS file.
