import React, { useState, useEffect } from "react";
import {
  loadCaptchaEnginge,
  LoadCanvasTemplate,
  validateCaptcha,
} from "react-simple-captcha";
import { Input } from "../../components/ui/input";
import logo from "../../assets/logo.svg";
import aadhaar from "../../assets/adhaar.svg";
import { Button } from "../../components/ui/button";
import { RefreshCw, Volume2 } from "lucide-react";

const Login = () => {

    const [aadhaarNumber, setAadhaarNumber] = useState("");
    const [captchaValue, setCaptchaValue] = useState("");
  
    useEffect(() => {
      loadCaptchaEnginge(5);
    }, []);
  
    const handleSubmit = (e: React.FormEvent) => {
      e.preventDefault();
      if(!aadhaarNumber){
        alert("Enter aadhar number")
        return;
      }
      if (validateCaptcha(captchaValue)) {
        alert("Login successful!");
      } else {
        alert("Invalid captcha. Please try again.");
        loadCaptchaEnginge(5);
        setCaptchaValue("");
      }
    };
  return (
    <>
    
      <div className="fixed top-0 left-0 z-9 w-full h-[70px] bg-white border-b-2 border-[#020B50] ">
        <div className="flex justify-between mx-auto max-w-[1170px] min-h-[65px] py-1 px-4 z-9999">
          <img src={logo} alt="Government of India Logo" className="h-12" />
          <img src={aadhaar} alt="Aadhaar Logo" className="h-12" />
        </div>
      </div>

      <section className="my-20 px-2">
        <div className="text-[#020B50] font-semibold py-1 px-2 text-center">
          Login to Aadhaar via OTP
        </div>
        <div className="relative mx-auto max-w-[400px] w-full rounded-lg shadow-lg overflow-hidden p-5">
          <div
            className="absolute top-0 left-0 w-full h-[5px] bg-gradient-to-r from-[#000046] to-[#1cb5e0]"
            aria-hidden="true"
          ></div>


          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <Input
                type="text"
                placeholder="Enter Aadhaar Number"
                value={aadhaarNumber}
                onChange={(e) => setAadhaarNumber(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded"
              />
            </div>
            <div className="flex items-center space-x-2">
              <Input
                type="text"
                placeholder="Enter Captcha"
                value={captchaValue}
                onChange={(e) => setCaptchaValue(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded"
              />
              <div className="flex items-center space-x-2 bg-gray-200 p-1 rounded">
                <LoadCanvasTemplate reloadText="" />
                <div className="flex flex-col space-y-1">
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    onClick={() => loadCaptchaEnginge(5)}
                    className="p-1 h-6 w-6"
                    aria-label="Reload captcha"
                  >
                    <RefreshCw className="h-4 w-4" />
                  </Button>
                  <Button
                    type="button"
                    variant="ghost"
                    size="icon"
                    className="p-1 h-6 w-6"
                    aria-label="Play audio captcha"
                  >
                    <Volume2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>
            <Button
              type="submit"
              className="bg-gradient-to-r from-[#020D51] to-[#19B0DC] text-white font-bold flex items-center justify-center w-full h-full bg-transparent border-none rounded transition-all duration-100 ease-linear text-center font-sans text-base capitalize"
            >
              Login With OTP
            </Button>
          </form>
        </div>
        <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded-md shadow-md mt-6">
          <h2 className="text-lg font-semibold mb-2">
            Warning: Privacy and Security
          </h2>
          <p>
            This website is a demonstration clone and is not affiliated with
            UIDAI or its official services. We take your privacy and security
            seriously. Any data captured on this site is used solely for the
            purpose of showcasing our machine learning model and improving user
            experience. No personal information is stored or shared. Please do
            not enter sensitive information.
          </p>
        </div>
        <footer className="fixed bottom-0 left-0 w-full bg-[#020348] py-3 z-5 text-white text-center">
        Copyright © 2024 Unique Identification Authority of India All Rights
        Reserved
      </footer>
      </section>
    </>
  );
};

export default Login;
