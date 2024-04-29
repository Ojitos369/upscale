import { useEffect } from 'react';
import { cambiarThema } from '../Core/helper';

import { Main } from '../Pages/Main';
import { Index } from '../Pages/Index';
import { Update } from '../Pages/Update';
import { Show } from '../Pages/Show';
import { Test } from '../Pages/Test';
import { Route, Routes, Navigate } from 'react-router-dom';

import { store } from './store';
import { Provider } from "react-redux";
import { useStates } from '../Hooks/useStates';


const BgTheme = () => {
    const { ls } = useStates();
    return (
        <>
            <div className={`wipeInDown full-page-container bg-my-${ls.theme}`}></div>
        </>
    )
}

function AppUI() {
    const { ls, s, f } = useStates();

    useEffect(() => {
        cambiarThema(ls?.theme);
    }, [ls?.theme]);

    useEffect(() => {
        const title = s.page?.title || "Upscale Images";
        document.title = title;
    }, [s.page?.title]);

    useEffect(() => {
        f.login.validateLogin();
    }, []);

    return (
        <div className={`text-[var(--my-minor)]`}>
            <BgTheme />
            <Routes>
                {/* -----------   Index   ----------- */}
                <Route path="" element={<Main />} >
                    <Route path="" element={<Index />} />
                    <Route path="update" element={<Update />} />
                    <Route path="show/:group" element={<Show />} />
                </Route>
                {/* -----------   /Index   ----------- */}
                {/* -----------   Test   ----------- */}
                <Route path="test" element={<Test />} />
                {/* -----------   /Test   ----------- */}

                {/* -----------   404   ----------- */}
                <Route path="*/" element={<div className='text-danger h1 text-center mt-5'>404 Not Found</div>} />
                {/* -----------   /404   ----------- */}

            </Routes>
        </div>
    );
}

function App(props) {
    return (
        <Provider store={store}>
            <AppUI />
        </Provider>
    );
}

export default App;
