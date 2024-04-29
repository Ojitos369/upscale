import { useMemo } from 'react';
import { Link } from 'react-router-dom';
import { useStates } from '../../../Hooks/useStates';

const MenuModal = props => {
    const { s, f, lf } = useStates();
    const { styles } = props;

    const userLogged = s.login?.data?.user || {};

    const login = () => {
        f.u2('menu', 'modal', 'mode', 'login');
    }
    
    return (
        <div className={`${styles.menuModal} w-full flex flex-wrap justify-center`}>
            <div className="w-10/12 md:w-5/12 px-4 py-3">
                <button
                    className='w-full flex items-center justify-center py-2 px-4 rounded-md bg-green-500 hover:bg-green-600 text-black'
                    onClick={lf.toggleTheme}
                    >
                    <p className="">Toggle Theme</p>
                </button>
            </div>
            {userLogged.token ?
            <div className="w-10/12 md:w-5/12 px-4 py-3">
                <Link
                    className='w-full flex items-center justify-center py-2 px-4 rounded-md bg-red-500 hover:bg-red-600 text-white'
                    to='/'
                    onClick={f.login.closeSession}
                    >
                    <p className="">Logout</p>
                </Link>
            </div> :
            <div className="w-10/12 md:w-5/12 px-4 py-3">
                <button
                    className='w-full flex items-center justify-center py-2 px-4 rounded-md bg-blue-500 hover:bg-blue-600 text-white'
                    onClick={login}
                    >
                    <p className="">Login</p>
                </button>
            </div>}
            <div className="w-10/12 md:w-5/12 px-4 py-3">
                <div
                    className='w-full flex items-center justify-center py-2 px-4 rounded-md bg-cyan-500 hover:bg-cyan-600 text-black'

                    >
                    <p className="">Filtros</p>
                </div>
            </div>
            <div className="w-10/12 md:w-5/12 px-4 py-3">
                <a
                    className='w-full flex items-center justify-center py-2 px-4 rounded-md bg-orange-500 hover:bg-orange-600 text-white'
                    href='https://me.ojitos369.com/#/contact/'
                    target='_blank'
                    rel='noreferrer'
                    >
                    <p className="">Contacto</p>
                </a>
            </div>
            {userLogged.token && 
            <div className={`w-10/12 px-4 py-3`}>
                <Link
                    className='w-full flex items-center justify-center py-2 px-4 rounded-md bg-purple-500 hover:bg-purple-600 text-black'
                    to='update'
                    onClick={() => {
                        f.u2('modals', 'header', 'showMenu', false);
                    }}
                    >
                    <p className="">New Image</p>
                </Link>
            </div>}
        </div>
    )
}

export { MenuModal }
