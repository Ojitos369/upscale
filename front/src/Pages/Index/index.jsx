import { useMemo } from 'react';
import { useStates } from '../../Hooks/useStates';
import { useEffect } from 'react';

import { InfoCard } from '../../Components/Cards/InfoCard';
import { DobleLoader } from '../../Components/Loaders/DobleLoader';
import { Paginacion } from '../../Components/Paginacion';

const Index = props => {
    const { ls, lf, s, f, Link } = useStates();

    const grupos = useMemo(() => s.app?.data?.grupos || [], [s.app?.data?.grupos]);
    const originales = useMemo(() => s.app?.data?.originales || [], [s.app?.data?.grupos]);
    const gettingImages = useMemo(() => !!s.loaders?.app?.getImages, [s.loaders?.app?.getImages]);

    const paginas = useMemo(() => s.app?.paginador?.paginas || 1, [s.app?.paginador?.paginas]);
    const pagina = useMemo(() => {
        let p = s.app?.paginador?.pagina || 1
        if (p > paginas) {
            return paginas;
        } else {
            return p;
        }
    }, [s.app?.paginador?.pagina]);

    const updatePage = page => {
        f.u2('app', 'paginador', 'pagina', page);
    }


    useEffect(() => {
        f.u2('app', 'show', 'images', null);
    }, []);

    if (gettingImages) {
        return (
            <div className='w-full flex justify-center mt-16'>
                <DobleLoader />
            </div>
        );
    }

    return (
        <div className='flex flex-wrap justify-center mb-5'>
            <Paginacion
                no_paginas={paginas || 1}
                pagina={pagina}
                funcion={updatePage}
            />
            {Object.keys(grupos).map((k,i) => {
                const g = grupos[k];
                const base = originales.filter(b => b?.group_image === k);
                const upscales = g.filter(u => u.model !== 'Original');
                const d = {...base[0], upscales};
                const unique = `show-${d.name}-${d.id_image}-${i}`;
                return (
                    <InfoCard
                        index={i + 1}
                        Link={Link}
                        {...d}
                        key={unique}
                    />
                )
            })}
            <Paginacion
                no_paginas={paginas || 1}
                pagina={pagina}
                funcion={updatePage}
            />
        </div>
    )
}

export { Index };
