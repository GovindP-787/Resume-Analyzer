import Navbar from "../components/navbar"
import Sidebar from "../components/sidebar"

const Dashboard = () => {
        return (
            <>
            <div className = "flex flex-row h-screen w-full bg-red-100" justify-between>
                <Sidebar/>
                <div className = "flex flex-col">
                    <Navbar/>
                </div> 
                
            </div>
            </>
        )
}
export default Dashboard