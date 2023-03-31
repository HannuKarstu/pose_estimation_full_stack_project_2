import React from "react";
import { Link } from "react-router-dom";

function Navbar() {
    return (
        <nav>
            <ul>
                <li>
                    <Link to="/">Results</Link>
                </li>
                <li>
                    <Link to="/prediction">Prediction</Link>
                </li>
                <li>
                    <Link to="/stats">Stats</Link>
                </li>
            </ul>
        </nav>
    );
}

export default Navbar;