import styles from '../styles/dobleLoader.module.scss';
const DobleLoader = props => {
    return (
        <div class={`${styles.dobleLoader}`}>
            <p class={`${styles.h2}`} >Loading....<span class={`${styles.lol}`}></span></p>
        </div>
    )
}
export { DobleLoader };