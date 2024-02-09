import React from 'react';
import { Link } from 'react-router-dom'; // Adjust based on your routing solution
import styles from './breadcrumbStyles.module.css'; // Corrected import path to CSS module

const Breadcrumbs = ({ breadcrumbItems }) => {
    return (
        <nav aria-label="breadcrumb">
            <ol className={styles.breadcrumb}>
                {breadcrumbItems.map((item, index) => (
                    <li key={index} className={`${styles['breadcrumb-item']} ${item.active ? styles.active : ''}`}>
                        {item.active ? item.label : <Link to={item.path}>{item.label}</Link>}
                    </li>
                ))}
            </ol>
        </nav>
    );
};

export default Breadcrumbs;
