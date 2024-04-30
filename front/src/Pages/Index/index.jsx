import { useMemo } from 'react';
import { useStates } from '../../Hooks/useStates';
import { useEffect } from 'react';

import { InfoCard } from '../../Components/Cards/InfoCard';

import { DobleLoader } from '../../Components/Loaders/DobleLoader';

const Index = props => {
    const { ls, lf, s, f, Link } = useStates();

    const grupos = useMemo(() => s.app?.data?.grupos || [], [s.app?.data?.grupos]);
    const originales = useMemo(() => s.app?.data?.originales || [], [s.app?.data?.grupos]);
    const gettingImages = useMemo(() => !!s.loaders?.app?.getImages, [s.loaders?.app?.getImages]);
    // console.log(originales);

    useEffect(() => {
        f.app.getCategorias();
    }, []);

    useEffect(() => {
        f.app.getImages();
    }, [s.app?.filtros]);

    if (!gettingImages) {
        return (
            <div className='w-full flex justify-center mt-16'>
                <DobleLoader />
            </div>
        );
    }

    return (
        <div className='flex flex-wrap justify-center mb-5'>
            {Object.keys(grupos).map((k,i) => {
                const g = grupos[k];
                const base = originales.filter(b => b?.group_image === k);
                const upscales = g.filter(u => u.model !== 'Original');
                const d = {...base[0], upscales};
                const unique = `show-${d.name}-${d.id_image}-${i}`;
                return (
                    <div key={unique} className={`w-10/12 md:w-1/4 flex justify-center px-3 ${unique}`} id={unique} >
                        <InfoCard
                            index={i + 1}
                            Link={Link}
                            {...d}
                        />
                    </div>
                )
            })}
        </div>
    )
}

export { Index };
