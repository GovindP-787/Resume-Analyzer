import Navbar from "../components/navbar";
import Sidebar from "../components/sidebar";
import {Outlet} from "react-router-dom";


export default function DashboardLayout() {
    return(
        <div className = "h-screen flex w-full">
            <Sidebar/>
            <div className = "flex min-w-0 flex-1 flex-col">
                <Navbar/>
                <div className = "flex-1 overflow-y-auto p-4 w-full ">
                    <Outlet/>
                </div>
            </div>
        </div>
    )
}
