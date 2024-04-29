import { useMemo } from 'react';
import { useStates } from '../../Hooks/useStates';

import './styles/index.module.css';
import { useEffect } from 'react';

const Index = props => {
    const { ls, lf, s, f } = useStates();

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
                    const { name, url, fecha_carga, model, scale, group_image, general_group } = base[0];
                    return (
                        <div key={i} className='w-5/12 md:w-1/3 p-2'>
                            <div className='border border-[var(--my-minor)] rounded-lg p-2'>
                                <img src={url} alt={name} className='w-full rounded-lg' />
                                <div className='p-2'>
                                    <h2 className='text-lg font-bold'>
                                        <a href={url} target='_blank' className='underline'>
                                            {name}
                                        </a>
                                        <span className='text-sm font-normal ml-5'>
                                            {general_group}
                                        </span>
                                    </h2>
                                    {/* <p>{model}</p>
                                    <p>{scale}</p> */}
                                    {/* <p>{group_image}</p> */}
                                    <div>
                                        <p className='m-0 p-0'>Upscales: </p>
                                        <p className='flex flex-row flex-wrap w-full mt-0 p-0'>
                                            {upscales.map((u, i) => {
                                                return (
                                                    <a key={i} href={u.url} target='_blank' className='mb-2 mr-3 underline'>
                                                        {u.name}- {u.model} - {u.scale}
                                                    </a>
                                                )
                                            })}
                                        </p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    )
                })}
            </div>
        </>
    )
}

export { Index };
