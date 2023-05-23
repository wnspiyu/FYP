import React from 'react'
import { Link } from 'react-router-dom'

import '../../App.css'

export default function SignUpPage() {

    return (
        <div className='center' style={{backgroundColor: "#8B008B" ,height: "50vh"}}>
            <div className='center' style={{ backgroundColor: "#191970" ,padding: "20px", width: "60%" }}>
                <div className="card">
                    <h2 style={{fontSize:30}}>SIGN UP</h2>
                    <h5>Create your account here</h5>
                    <form action="/home">
                        <p>
                            <label>Username</label><br/>
                            <input type="text" name="first_name" required style={{ width: "100%",padding:"5px" }} />
                        </p>
                        <p>
                            <label>Email address</label><br/>
                            <input type="email" name="email" required style={{ width: "100%",padding:"5px" }}/>
                        </p>
                        <p>
                            <label>Password</label><br/>
                            <input type="password" name="password" style={{ width: "40%",padding:"5px" }} requiredc />
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
        </div>
    )

}
