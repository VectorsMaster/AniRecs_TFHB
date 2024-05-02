import axios from "axios";
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

const SingUp = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const onSignUp = () => {
    const body = new URLSearchParams();
    body.append("username", userName);
    body.append("password", password);

    axios
      .post("http://localhost:8000/sign_up/", body)
      .then((r) => {
        if (r.status === 200) {
          toast.success(`Try to log in now!`);
          navigate("/login");
        }
      })
      .catch((e) => {
        if (e.response.data.detail) {
          toast.error(e.response.data.detail);
        } else {
          toast.error("Unknown error, please try again later");
        }
      });
  };

  return (
    <div className={"mainContainer"}>
      <div className={"titleContainer"}>
        <div>Signup</div>
      </div>
      <br />
      <div className={"inputContainer"}>
        <input
          value={userName}
          placeholder="Enter your username here"
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
          className={"inputBox"}
        />
      </div>
      <br />
      <div className={"inputContainer"}>
        <input
          className={"inputButton"}
          type="button"
          onClick={onSignUp}
          value={"Sign up"}
        />
      </div>
      Already have an account? <Link to="/login">LogIn</Link>
    </div>
  );
};

export default SingUp;
