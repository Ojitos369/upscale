import { Outlet } from 'react-router-dom';
import { useMemo, useEffect } from 'react';
import { useStates } from '../../Hooks/useStates';
import styles from './styles/index.module.scss';

import { Header } from '../../Components/Header';

const Main = props => {
    const { f, s  } = useStates();

    const paginas = useMemo(() => s.app?.paginador?.paginas || 1, [s.app?.paginador?.paginas]);
    const pagina = useMemo(() => {
        let p = s.app?.paginador?.pagina || 1
        if (p > paginas) {
            return paginas;
        } else {
            return p;
        }
    }, [s.app?.paginador?.pagina]);
    const por_pagina = useMemo(() => s.app?.paginador?.por_pagina || 20, [s.app?.paginador?.por_pagina]);

    useEffect(() => {
        f.app.getCategorias();
    }, []);

    useEffect(() => {
        f.app.getImages();
    }, [s.app?.filtros, pagina, por_pagina]);

    return (
        <div className={styles.container}>
            <Header />
            <Outlet />
        </div>
    )
}

export { Main };