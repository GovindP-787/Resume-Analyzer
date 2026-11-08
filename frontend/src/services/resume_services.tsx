import axios from "axios";
const api = axios.create({baseURL:"http://127.0.0.1:8000"})

export const uploadResume = async (file: File, userId: number) =>{
    const formData = new FormData();
    formData.append("file",file);
    formData.append("user_id",userId.toString());

    
    const response = await api.post("/resume/fileupload",formData)
    return response.data;
};

export const analyseResume = async (resumeId: number, jobdescription: string)=>{
    const response = await api.post(`/resume/${resumeId}/analyse`,{job_description:jobdescription});
    return response.data;

}