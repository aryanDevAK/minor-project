import React from 'react'
import "./Patient.css"
import delete_icon from "../../assets/delete.png"
import edit_icon from "../../assets/edit.png"
import view_icon from "../../assets/view.png"

const Patient = () => {
    return (
<table className='w-full border-separate border-spacing-2'>
    <thead>
      <tr>
        <th className='border border-slate-600 rounded-md '>ID</th>
        <th className='border border-slate-600 rounded-md'>Name</th>
        <th className='border border-slate-600 rounded-md max-md:hidden'>Mobile Number</th>
        <th className='border border-slate-600 rounded-md max-md:hidden'>Recent Appointments</th>
        <th className='border border-slate-600 rounded-md'>Operations</th>
      </tr>
    </thead>
    <tbody>
        <tr className='h-8'>
          <td className='border border-slate-700 rounded-md text-center'></td>
          <td className='border border-slate-700 rounded-md text-center'></td>
          <td className='border border-slate-700 rounded-md text-center max-md:hidden'></td>
          <td className='border border-slate-700 rounded-md text-center max-md:hidden'></td>
          <td className='border border-slate-700 rounded-md text-center'>
            <div className='operations flex justify-evenly gap-x-4'>
                <img src={view_icon} alt="" />
                <img src={edit_icon} alt="" />
                <img src={delete_icon} alt="" />
            </div>
          </td>
        </tr>
    </tbody>
  </table>
  )
}

export default Patient