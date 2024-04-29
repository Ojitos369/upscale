import { useMemo } from 'react';
import { useStates } from '../../Hooks/useStates';
import styles from './styles/index.module.scss';

const Update = props => {
    const { l, s  } = useStates();
    const userLogged = useMemo(() => s.login?.data?.user || {}, [s.login?.data?.user]);

    if (!userLogged.token) {
        return (
            <div className='w-full flex justify-center'>
                <p className='text-3xl font-bold'>
                    Not logged
                </p>
            </div>
        );
    }

    return (
        <div className={styles.container}>
            <h1>Update</h1>
        </div>
    )
}

export { Update };