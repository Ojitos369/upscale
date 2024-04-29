import { useMemo } from 'react';
import { useStates } from '../../Hooks/useStates';
import { useEffect } from 'react';

import { InfoCard } from '../../Components/Cards/InfoCard';

const Index = props => {
    const { ls, lf, s, f, Link } = useStates();

    const grupos = useMemo(() => s.app?.data?.grupos || [], [s.app?.data?.grupos]);
    const originales = useMemo(() => s.app?.data?.originales || [], [s.app?.data?.grupos]);

    useEffect(() => {
        f.app.getCategorias();
        f.app.getImages();
    }, []);
    return (
        <>
            <div className='flex flex-wrap justify-center'>
                {Object.keys(grupos).map((k,i) => {
                    const g = grupos[k];
                    // console.log(g);
                    const base = originales.filter(b => b.group_image === k);
                    const upscales = g.filter(u => u.model !== 'Original');
                    const d = {...base[0], upscales};
                    return (
                        <div key={i} className="w-10/12 md:w-1/4 flex justify-center px-3">
                            <InfoCard
                                index={i + 1}
                                Link={Link}
                                {...d}
                            />
                        </div>
                    )
                })}
            </div>
        </>
    )
}

export { Index };
