import { Outlet } from 'react-router-dom';
import { useStates } from '../../Hooks/useStates';
import styles from './styles/index.module.scss';

import { Header } from '../../Components/Header';

const Main = props => {
    const { l, s  } = useStates();

    return (
        <div className={styles.container}>
            <Header />
            <Outlet />
        </div>
    )
}

export { Main };