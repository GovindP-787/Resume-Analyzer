import files from "../assets/files.svg"
import layout from "../assets/layout.svg"
import history from "../assets/history.svg"
import settings_icon from "../assets/settings_icon.svg"
import file_icon from "../assets/file_icon.svg"
import sparkles from "../assets/sparkles.svg"
import logout from "../assets/logout.svg"
import {NavLink} from "react-router-dom"


const Sidebar = () =>{
    return(
        <>
        <div className = "w-[248px] shrink-0 h-screen bg-[#FFFFFF] border-r border-[#EAE8EF] flex flex-col items-center px-4.5 justify-between relative">
            <div className = "w-full flex flex-col items-center gap-6 p-px mt-5">
                <div className = "w-full h-8" >
                    <h1 className = "text-[21px] font-bold font-inter"><span>Resu</span>Mate</h1>    {/*Logo of the application */}
                </div>
                <div className = "w-full flex flex-col gap-1.5">
                    <div className = "w-full h-12 bg-[#F5F5F5] rounded-lg flex items-center   gap-3 p-1">
                       <img src={layout} alt="layout" className = "w-5 h-5 ml-3 "/>
                       <p className = "font-inter font text-[13px] font-semibold text-center w-[60%] text-[#565161]">Dashborad</p>
                        
                    </div>
                    <div className = "w-full h-12 bg-[#F5F5F5] rounded-lg flex items-center gap-3">
                        <img src={file_icon} alt="files" className = "w-5 h-5 ml-3"/>
                        <p className = "font-inter font text-[13px] font-semibold w-[60%] text-center text-[#565161]">Analysis</p>
                    </div>
                    <div className = "w-full h-12 bg-[#F5F5F5] rounded-lg flex items-center  gap-3">
                        <img src={history} alt="history" className = "w-5 h-5 ml-3"/>
                        <p className = "font-inter font text-[13px] font-semibold w-[60%] text-center text-[#565161]">Analysis History</p>
                    </div>
                    <div className = "w-full h-12 bg-[#F5F5F5] rounded-lg flex items-center  gap-3">
                        <img src={files} alt="settings" className = "w-5 h-5 ml-3"/>
                        <p className = "font-inter font text-[13px] font-semibold w-[60%] text-center text-[#565161]">My Resumes</p>
                    </div>
                    <div className = "w-full h-12 bg-[#F5F5F5] rounded-lg flex items-center  gap-3">
                        <img src={settings_icon} alt="settings" className = "w-5 h-5 ml-3"/>
                        <p className = "font-inter font text-[13px] font-semibold w-[60%] text-center text-[#565161]">Settings</p>
                    </div>
                </div>

            </div>
            <div className = "w-full h-54 gap-4 flex flex-col items-center justify-center mb-2 ">
                <div className= "w-full h-25 rounded-xl gap-2 bg-[#F5F3FF] flex flex-col items-center justify-center p-4">
                    <div className = "w-full flex items-center gap-2">
                        <img src={sparkles} alt="sparkles" className = "w-3.2 h-3.2 "/>
                        <p className = "font-inter font text-3 font-semibold w-[80%]  text-center text-[#7C3AED] ">A clearer next step</p>
                    </div>
                   <p className = "font-inter font text-[13px] font-normal w-full text-start text-[#565161]">Turn your experience into your next opportunity.</p>
                </div>
                

                
                    <div className = "w-full h-9.2 flex gap-2 items-center">
                        <div className = "w-10 h-8 bg-[#bab9ee] rounded-full flex items-center justify-center">
                            <h1>GP</h1>
                        </div>
                        <div className ="w-full h=9.2 flex flex-col gap-0.5 items-start justify-center">
                            <p className = "font-inter font text-[13px] font-semibold w-full text-start text-[#000000]">John Doe</p>
                            <p className = "font-inter font text-[11px] font-normal w-full text-start text-[#565161]">Email</p>
                        </div>
            
                    </div>
                     <div className = "w-full h-4 flex items-center gap-2 justify-center">
                        <img src={logout} alt="logout" className = "w-4.5 h-4.5 ml-2"/>
                        <p className = "font-inter font text-[12px] font-normal w-full text-start text-[#565161]">Logout</p>
                        </div>
            
            </div>
            <button className = "rounded-full absolute w-6 h-6 top-2 right-2 bg-black text-white flex justify-center items-center">o</button>
        </div>
        </>
    )
}
export default Sidebar