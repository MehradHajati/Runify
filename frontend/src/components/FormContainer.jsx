import React from "react";
import FormBox from "./FormBox";

const FormContainer = ({ formTitle, buttonText }) => {
  return (
    <div className="w-[530px] max-md:w-full max-md:max-w-[530px]">
      <FormBox title={formTitle} buttonText={buttonText} />
    </div>
  );
};

export default FormContainer;