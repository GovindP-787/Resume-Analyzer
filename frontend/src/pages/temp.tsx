import React from "react";
import { useState } from "react";

import { uploadResume, analyseResume } from "../services/resume_services";
const ResumeAnalysis = ()=>{

    const [loading,setLoading] = useState(false)
    const [error,setError] = useState("")
    const [file,setFile] = useState <File | null>(null)
    const [jobDescription,setJobDescription] = useState("")
    const [result,setResult] = useState<any>(null)

    const handleSubmit = async () =>{
        if(!file || !jobDescription.trim()){
            setError("upload both resume and jd")
            return;
        }
        try{
            setLoading(true)
            setError("")
            setResult(null)

            const uploadResponse = await uploadResume(file,4)
            console.log("upload_response", uploadResponse)
            const resumeId = uploadResponse.resume_id;
            console.log("resume id", resumeId)

            if (!resumeId) {
    throw new Error("Resume ID was not returned by the upload API");
}
            const uploadAnalysis = await analyseResume(resumeId,jobDescription)
          
            setResult(uploadAnalysis)


        } catch (err) {
            console.error(err);
            setError("Something went wrong. Please try again.");
        } finally {
            setLoading(false);
        }
    
    };


return(
    <>
    <div className = "w-screen h-screen p-4 bg-red-100">
        <h1 className = "text-inter text-3xl m-3">Resume Analyser - First Deliverable</h1>
        <div className = "w-full bg-red-200 flex  justify-evenly">
            <div className = "flex justify-center items-center p-3 border-2 w-100 h-100">
                <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files?.[0] ?? null)}
                className = "h-full w-full rounded bg-amber-50 "></input>
                
            </div>
            <div className = "p-3 border-2 w-100 h-100">
                <textarea placeholder="job description" className="bg-amber-50 w-full h-full " value={jobDescription} onChange={(e)=>setJobDescription(e.target.value)}></textarea>
            
        </div>
        </div>
         <button className="w-30 h-10 border-2 rounded-2xl cursor-pointer " onClick={handleSubmit} disabled={loading}>
                {loading ? "Analyzing..." : "Analyze Resume"}
                 
            </button>
         {result && (
                <pre>
                    {JSON.stringify(result, null, 2)}
                </pre>
            )}
        
        
    </div>
    
    </>
)
}

export default ResumeAnalysis