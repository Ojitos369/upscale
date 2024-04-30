import { useEffect, useMemo } from 'react';
import { useStates } from '../../Hooks/useStates';
import { Phone } from '../../Components/Cards/Phone';
import { DownloadIcon } from '../../Components/Icons';
import styles from './styles/index.module.scss';

const Show = props => {
    const { ls, lf, s, f, useParams } = useStates();

    const images = useMemo(() => s.app?.show?.images || [], [s.app?.show?.images]);
    // console.log(images);

    const { group } = useParams();

    const download = url => {
        const name = url.split('/').pop();
        const a = document.createElement('a');
        a.href = url;
        a.download = name;
        a.click();
    };

    useEffect(() => {
        // f.u2('app', 'filtros', 'group', group);
        f.app.getGroupImages(group);
    }, [group]);

    return (
        <div className='flex flex-wrap justify-around'>
            <h2 className='w-full text-center mt-5 text-2xl font-bold'>
                {group}
            </h2>
            {images.map((image, index) => {
                return (
                    <div className='mt-8 mx-5 w-auto flex flex-col items-center' key={index}>
                        <Phone key={index} image={image} />
                        <div className={`${styles.downloadLabel} text-start border rounded-lg px-4 py-2 mt-2`}>
                            <a href={image.url} target='_blank' rel='noreferrer' className='text-blue-500 underline'>
                                {image.name} - {image.scale}
                            </a>
                            <span className={`${styles.downloadIcon}`}>
                                <DownloadIcon onClick={() => download(image.url)} />
                            </span>
                        </div>
                    </div>
                )
            })}
        </div>
    )
}

export { Show };
