import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import axios from "axios";
import { toast } from "react-toastify";

const SignIn = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const SingIn = async () => {
    const body = new URLSearchParams();
    body.append("username", userName);
    body.append("password", password);

    axios
      .post("http://localhost:8000/token", body)
      .then((r) => {
        if (r.status === 200) {
          toast.success(`Welcome back ${userName}!`);
          localStorage.setItem("token", r.data.access_token);
          navigate("/");
        }
      })
      .catch((e) => {
        if (e.response.status === 401) {
          toast.error("Wrong username or password");
        } else {
          toast.error("Network problem, please try again");
        }
      });
  };

  return (
    <div className={"mainContainer"}>
      <div className={"titleContainer"}>
        <div>Login</div>
      </div>
      <br />
      <div className={"inputContainer"}>
        <input
          value={userName}
          placeholder="Enter your email here"
          onChange={(ev) => setUserName(ev.target.value)}
          className={"inputBox"}
        />
      </div>
      <br />
      <div className={"inputContainer"}>
        <input
          value={password}
          type="password"
          placeholder="Enter your password here"
          onChange={(ev) => setPassword(ev.target.value)}
          className="inputBox"
        />
      </div>
      <br />
      <div className="inputContainer">
        <input
          className="inputButton"
          type="button"
          onClick={SingIn}
          value="Log in"
        />
      </div>
      Don't have an account? <Link to="/signup">SignUp</Link>
    </div>
  );
};

export default SignIn;
