import {Link} from "react-router-dom";
import React from "react";
import PropTypes from "prop-types";

/**
 *
 * Simple Navigation item for navigation bars
 * @return {JSX.Element}
 *
 * @memberOf components.common
 * @component
 */
let NavItem = props => {
    let options = {};
    if (props.onClick) {
        options.onClick = props.onClick;
        options.to = props.pageURI;
    } else if (props.path) {
        options.to = props.path;
    }
    if (props.brand){
        return (
            <Link 
                className="navbar-brand"
                onClick={props.onClick}
                {...options}
            >
                {props.children}
            </Link>
        )
    }
    return (
        <li
            
        >
            <Link
                {...options}
                className={
                    (props.disabled ? 'nav-link disabled' : 'nav-link') + ' ' +
                    (props.path === props.pageURI ? 'nav-item active font-weight-bold' : 'nav-item')
                }
            >
                {props.children}   
            </Link>
        </li>
    );
}

NavItem.propTypes = {
    /**
     * The path to compare to in order to find out, if this NavItem
     * has a link to the page, that is currently active
     */
    path: PropTypes.string,
    /**
     * The URL of the current active page
     */
    pageURI: PropTypes.string.isRequired,
    /**
     * The NavItem is displayed with muted/dimmed text
     */
    disabled: PropTypes.bool,
    /**
     * The name that should primarily be displayed on the item
     */
    name: PropTypes.string,
    /**
     * Set true to specify, that this NavItem should be displayed bigger
     * normally put to the left or to the right of the navigation bar
     */
    brand: PropTypes.bool,
}
NavItem.defaultProps = {
    path: '/',
    pageURI: '/',
    disabled: false,
    brand: false,
    dynamic: false
}

export default NavItem;