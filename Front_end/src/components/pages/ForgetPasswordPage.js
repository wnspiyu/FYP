import React from 'react'
import { Link } from 'react-router-dom'

import '../../App.css'

export default function ForgetPasswordPage() {
    return (
        <div className='center' style={{backgroundColor: "purple" ,height: "50vh"}}>
            <div className="center" style={{ backgroundColor: "#191970" ,padding: "20px", width: "60%" }}>
                <div className="card">
                    <h2 style={{fontSize:25}}>Reset your password</h2><br></br>
                    <h5>Enter your email address and we will send you a new password</h5>
                    <form action="/login">
                        <p>
                            <label id="reset_pass_lbl">Email address</label>
                            <input type="email" name="email" required style={{ width: "100%",padding:"5px" }}/><br></br>
                        </p>
                        <p>
                            <center><button id="sub_btn" type="submit" style={{ width: "250px" }}>Send password reset email</button></center>
                        </p>
                    </form>
                    <footer>
                        <p style={{fontSize:15}}>First time? <Link to="/register">Create an account</Link>.</p>
                        <p style={{fontSize:15}}><Link to="/">Back to Homepage</Link>.</p>
                    </footer>
                </div>    
            </div>
        </div>
    )
}
