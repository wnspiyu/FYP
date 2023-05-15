import React from 'react'
import { Link } from 'react-router-dom'

import '../../App.css'

export default function SignUpPage() {

    return (
        <div className='center' style={{ padding: "20px", width: "50%" }}>
            <div className="card">
                <h2>Join us</h2>
                <h5>Create your personal account</h5>
                <form action="/home">
                    <p>
                        <label>Username</label><br/>
                        <input type="text" name="first_name" required />
                    </p>
                    <p>
                        <label>Email address</label><br/>
                        <input type="email" name="email" required style={{ width: "100%" }}/>
                    </p>
                    <p>
                        <label>Password</label><br/>
                        <input type="password" name="password" requiredc />
                    </p>
                    <p>
                        <input type="checkbox" name="checkbox" id="checkbox" required /> <span>I agree all statements in <a href="https://google.com" target="_blank" rel="noopener noreferrer">terms of service</a></span>.
                    </p>
                    <br/>
                    <p>
                        <center><button id="sub_btn" type="submit"style={{ width: "250px" }}>Register</button></center>
                    </p>
                </form>
                <footer>
                    <p style={{ fontSize: "15px" }}><Link to="/">Back to Homepage</Link>.</p>
                </footer>
            </div>
        </div>
    )

}
