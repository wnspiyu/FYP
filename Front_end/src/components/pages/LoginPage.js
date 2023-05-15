import React from 'react'
import { Link } from 'react-router-dom'

import '../../App.css'

export default function SignInPage() {
    return (
        <div className='center' style={{ padding: "20px", width: "50%" }}>
            <div className="card">
                <h2>Sign in</h2>
                <form action="/home">
                    <p>
                        <label>Username or email address</label><br />
                        <input type="text" name="first_name" required />
                    </p>
                    <p>
                        <label>Password</label>
                        <input type="password" name="password" required />
                        <Link to="/forget-password"><label className="left-label">Forget password?</label></Link>
                        {/* <br /> */}
                    </p>
                    <p>
                    <center><button id="sub_btn" type="submit"style={{ width: "200px" }}>Login</button></center>
                    </p>
                </form>
                <footer>
                    <p style={{ fontSize: "15px" }}>First time? <Link to="/register">Create an account</Link>.</p>
                    <p style={{ fontSize: "15px" }}><Link to="/">Back to Homepage</Link>.</p>
                </footer>
            </div>
        </div>
    )
}
