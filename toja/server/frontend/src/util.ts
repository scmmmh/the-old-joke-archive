export function dateIntoParts(date: string): string[] {
    const parts = date.split('-');
    if (parts.length === 1) {
        return [parts[0], undefined, undefined];
    } else if (parts.length === 2) {
        return [parts[0], parts[1], undefined];
    } else if (parts.length >= 3) {
        return parts.slice(0, 3);
    }
}

export function yearFromDate(date: string): string | undefined {
    return dateIntoParts(date)[0];
}

export function monthToHuman(month: string): string | undefined {
    if (month === '01') {
        return 'January';
    } else if (month === '02') {
        return 'February';
    } else if (month === '03') {
        return 'March';
    } else if (month === '04') {
        return 'April';
    } else if (month === '05') {
        return 'May';
    } else if (month === '06') {
        return 'June';
    } else if (month === '07') {
        return 'July';
    } else if (month === '08') {
        return 'August';
    } else if (month === '09') {
        return 'September';
    } else if (month === '10') {
        return 'October';
    } else if (month === '11') {
        return 'November';
    } else if (month === '12') {
        return 'December';
    }
}

export function dayToHuman(day: string): string {
    const dayNr = Number.parseInt(day);
    if (dayNr === 1 || dayNr === 21 || dayNr === 31) {
        return dayNr + 'st';
    } else if (dayNr === 2 || dayNr === 22) {
        return dayNr + 'nd';
    } else if (dayNr === 3 || dayNr === 23) {
        return dayNr + 'rd';
    } else {
        return dayNr + 'th';
    }
}

export function monthDayFromDate(date: string): string | undefined {
    const parts = dateIntoParts(date);
    if (parts[1] && parts[2]) {
        return monthToHuman(parts[1]) + ' ' + dayToHuman(parts[2]);
    } else if(parts[1]) {
        return monthToHuman(parts[1]);
    } else {
        return undefined;
    }
}
