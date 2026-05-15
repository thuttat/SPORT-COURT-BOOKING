import React from "react";
import { Card, CardContent } from "../../../../components/common/Card.jsx";
import { EmptyState } from "../../../../components/common/EmptyState.jsx";
import { sportIcons } from "../../../../utils/constants.jsx";
import { capitalizeFirstLetter } from "../../../../utils/formatters.js";

export function SportDistribution({ fields }) {
    const sportCounts = fields.reduce((acc, field) => {
        const sport = field.field_type ? field.field_type.toLowerCase() : "default";
        acc[sport] = (acc[sport] || 0) + 1
        return acc;
    }, {});

    return (
        <Card>
            <CardContent className="content">
                <h3>Fields by Sport</h3>
                <div className="sport-list">
                    {Object.entries(sportCounts).map(([sport, count]) => (
                        <div key={sport} className="sport-item">
                            <div className="sport-row">
                                <div className="sport-name">
                                    <span className="sport-icon">
                                        {sportIcons[sport]}
                                    </span>
                                    <span>
                                        {capitalizeFirstLetter(sport)}
                                    </span>
                                </div>

                                <span className="sport-count">
                                    {count}
                                </span>
                            </div>

                            <div className="progress">
                                <div
                                    className={`progress-bar ${sport}`}
                                    style={{
                                        width: `${fields.length ? (count / fields.length) * 100 : 0}%`,
                                    }}
                                />
                            </div>
                        </div>
                    ))}

                    {fields.length === 0 && (
                        <EmptyState text="fields" />
                    )}
                </div>
            </CardContent>
        </Card>
    );
}