import { useMemo } from 'react';
import { useStates } from '../../../Hooks/useStates';
import { useKeyDown, useKeyUp, useLocalTab } from '../../../Hooks/myHooks';
import { Stair } from '../../Loaders/Stair';
import { useEffect } from 'react';
import { ChevronsLeft } from '../../Icons';

const ListenKeys = props => {
    const { keyExec } = props;
    // ---------------------------------------------   KEYBOARD EVENTS   --------------------------------------------- #
    useKeyDown(props.closeFiltros, ['escape'], keyExec);
    useKeyUp(null, ['any'], keyExec);
    // ---------------------------------------------   /KEYBOARD EVENTS   --------------------------------------------- #

    return null;
}

const Filtros = props => {
    const { s, f } = useStates();
    const { styles } = props;
    const keyExec = s.menu?.modal?.mode === 'filtros';
    const messageError = useMemo(() => s.menu?.filtros?.error || '', [s.menu?.filtros?.error]);
    const loading = useMemo(() => !!s.loaders?.filtros?.filtros || '', [s.loaders?.filtros?.filtros]);
    const filtros = useMemo(() => !!s.menu?.filtros?.filtros || '', [s.menu?.filtros?.filtros]);
    // const messageError = s.menu?.filtros?.error || '';

    const closeFiltros = () => {
        console.log("saliendo filtros")
        f.u2('menu', 'modal', 'mode', 'menu');
    }

    const filtrar = e => {
        if (!!e) e.preventDefault();
        f.u1('app', 'filtros', {...s.app?.filtros, ...s.menu?.filtros});
        closeFiltros();
    }

    const updateFiltros = e => {
        f.u3('menu', 'filtros', 'filtros', e.target.name, e.target.value);
    }

    useEffect(() => {
        f.u2('menu', 'filtros', 'error', '');
    }, []);

    if (loading) {
        return (
            <div className='my-5 w-full flex justify-center'>
                <Stair />
            </div>
        );
    }
    
    return (
        <>
            {keyExec && 
            <ListenKeys 
                keyExec={keyExec}
                closeFiltros={closeFiltros}
            />}
            <span className='w-[30px] m-3'>
                <ChevronsLeft
                    onClick={closeFiltros}
                    />
            </span>

            {/* name, model, fi, ff, scale, gi, gg, cats, por_pagina */}
            <form 
                className={`${styles.filtros} w-full flex flex-col items-center mt-2`}
                onSubmit={filtrar}
                >
                <p className='w-full text-center text-3xl font-bold'>
                    Filtros
                </p>

                <div className={`${styles.input_element}`}>
                    <label className={`${styles.input_label}`} htmlFor="">Nombre</label>
                    <input 
                        className={`${styles.input}`} 
                        type="text"
                        name='name'
                        value={s.menu?.filtros?.name || ''}
                        onChange={updateFiltros}
                        />
                </div>

                <div className={`${styles.submit_element}`}>
                    <input
                        type='submit'
                        className={`${styles.input_button} bg-blue-500 hover:bg-blue-600`}
                        value='Filtros'
                        />
                </div>

                {messageError &&
                <div className={`${styles.error_message}`}>
                    <small className={`${styles.message}`}>
                        {messageError}
                    </small>
                </div>
                }
            </form>
        </>
    )
}

export { Filtros }
