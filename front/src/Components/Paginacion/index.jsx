import { useStates } from '../../Hooks/useStates';
import styles from './styles/index.module.scss'
const Paginacion = props => {
    const { ls, s, f } = useStates();
    const { no_paginas, pagina } = props;
    const ejecutar = props.funcion;

    if (no_paginas > 1) {
        return (
            <div 
                className={`flex justify-start w-full mt-5 ${styles.paginacion_row}`}>
                <div className={`flex justify-start w-10/12 ${styles.paginacion}`}>
                    {pagina > 1 && 
                    <button 
                        className={`flecha ${styles.paginacion_item} reflejo${ls.theme === 'white' ? '-white': ''}`}
                        onClick={() => {
                            ejecutar(pagina - 1);
                        }}>
                        <span>&laquo;</span>
                    </button>}

                    
                    {(no_paginas > 2 && pagina > 2) &&
                    <button 
                        className={`${styles.paginacion_item} reflejo${ls.theme === 'white' ? '-white': ''}`}
                        onClick={() => {
                            ejecutar(1);
                        }}>
                        <p >
                            1
                        </p>
                    </button>}

                    
                    {(no_paginas > 1 && pagina > 1) &&
                    <button 
                        className={`${styles.paginacion_item} reflejo${ls.theme === 'white' ? '-white': ''}`}
                        onClick={() => {
                            ejecutar(pagina - 1);
                        }}>
                        <p>
                            { pagina - 1 }
                        </p>
                    </button>}

                    <button 
                        className={`${styles.paginacion_item} ${styles.paginacion_item_active}`}
                        disabled>
                        <p>
                            { pagina }
                        </p>
                    </button>

                    
                    {(no_paginas > 1 && pagina < no_paginas) &&
                    <button 
                        className={`${styles.paginacion_item} reflejo${ls.theme === 'white' ? '-white': ''}`}
                        onClick={() => {
                            ejecutar(pagina + 1);
                        }}>
                        <p>
                            { pagina + 1 }
                        </p>
                    </button>}

                    
                    {(no_paginas > 2 && pagina < no_paginas - 1) &&
                    <button 
                        className={`${styles.paginacion_item} reflejo${ls.theme === 'white' ? '-white': ''}`}
                        onClick={() => {
                            ejecutar(no_paginas);
                        }}>
                        <p>
                            { no_paginas }
                        </p>
                    </button>}
                    
                    
                    {pagina < no_paginas &&
                    <button 
                        className={`flecha ${styles.paginacion_item} reflejo${ls.theme === 'white' ? '-white': ''}`}
                        onClick={() => {
                            ejecutar(pagina + 1);
                        }}>
                        <span>&raquo;</span>
                    </button>}
                </div>
            </div>
        )
    } else {
        return null;
    }
}

export { Paginacion };